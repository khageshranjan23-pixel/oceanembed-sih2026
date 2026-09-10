import csv,json,collections,pathlib,hashlib,sys,numpy as np,xarray as xr,zipfile
root=pathlib.Path(sys.argv[1]).resolve() if len(sys.argv)>1 else pathlib.Path(__file__).resolve().parents[3]
out=pathlib.Path(__file__).resolve().parents[1]/'server/data'
dates=collections.Counter(); grids={}; missing=np.zeros(15,dtype=int);rows=0
for r in csv.DictReader(open(root/'reconstructions.csv')):
 vals=[None if v=='NULL' else float(v) for v in r['temperature_c'][1:-1].split(',')];unc=[None if v=='NULL' else float(v) for v in r['uncertainty_c'][1:-1].split(',')]
 assert len(vals)==len(unc)==15
 dates[r['obs_date']]+=1;rows+=1;missing+=np.array([v is None for v in vals]);grids.setdefault(r['obs_date'],set()).add((float(r['lat']),float(r['lon'])))
points=sorted(grids[min(grids)]);same=all(set(points)==x for x in grids.values())
assert same
coverage={'dates':sorted(dates),'profiles':rows,'profiles_per_day':dict(dates),'points':points,'depths':[0,5,10,20,30,50,75,100,125,150,200,300,500,700,1000],'source':'Supplied reconstructions.csv; precomputed outputs','max_matching_distance_km':25,'missing_per_depth':missing.tolist()}
(out/'coverage.json').write_text(json.dumps(coverage,separators=(',',':')))
metrics=[]
for r in csv.DictReader(open(root/'regime_metrics.csv')):metrics.append({'depth_m':int(float(r['depth_m'])),'rmse_c':float(r['rmse']),'bias_c':float(r['bias']),'correlation':float(r['correlation']),'n_points':int(r['n_points']),'regime':r['regime'],'validation_target':r['validation_target']})
(out/'metrics.json').write_text(json.dumps(metrics))
cases=[]
for r in csv.DictReader(open(root/'inversion_case_studies.csv')):
 for k in ['lat','lon','depth_m','raw_argo_temp','glorys_temp','model_temp']:r[k]=float(r[k]) if r[k] else None
 cases.append(r)
(out/'cases.json').write_text(json.dumps(cases,allow_nan=False))
ds=xr.open_dataset(root/'satyam/oceanembed_cube.nc');findings={'profiles':rows,'dates':[min(dates),max(dates)],'same_grid_each_date':same,'locations':len(points),'missing_per_depth':missing.tolist(),'cube_variables':list(ds.data_vars),'cube_attributes':ds.attrs,'argo_depths':ds.argo_depth.values.tolist(),'case_source_checks':[]}
for r in cases:
 c=ds.sel(time=r['obs_date'],lat=r['lat'],lon=r['lon'])
 g=float(c.glorys_temperature.sel(depth=r['depth_m']).values)
 a=float(c.argo_temperature.sel(argo_depth=r['depth_m']).values) if r['depth_m'] in ds.argo_depth else float('nan')
 findings['case_source_checks'].append({'date':r['obs_date'],'depth':r['depth_m'],'glorys_matches_cube':(r['glorys_temp'] is None and np.isnan(g)) or (r['glorys_temp'] is not None and abs(r['glorys_temp']-g)<1e-8),'argo_cube_finite':bool(np.isfinite(a))})
# Verify the stored climatology against a full-series harmonic fit at representative valid columns.
t=np.arange(ds.sizes['time']);doy=ds.time.dt.dayofyear.values;X=np.column_stack([np.ones(len(t)),np.sin(2*np.pi*doy/365.25),np.cos(2*np.pi*doy/365.25),np.sin(4*np.pi*doy/365.25),np.cos(4*np.pi*doy/365.25)])
checks=[]
for la,lo in [(14.375,88.125),(15.125,68.125)]:
 c=ds.sel(lat=la,lon=lo,depth=100);y=c.glorys_temperature.values;cl=c.climatology.values;m=np.isfinite(y)
 if m.any():
  pred=X@np.linalg.lstsq(X[m],y[m],rcond=None)[0];checks.append({'lat':la,'lon':lo,'max_full_series_harmonic_difference':float(np.nanmax(abs(cl-pred)))})
findings['climatology_fit_checks']=checks
findings['sha256']={f:hashlib.sha256((root/f).read_bytes()).hexdigest() for f in ['regime_metrics.csv','inversion_case_studies.csv','OceanEmbed_Training.ipynb']}
(root/'front_end/ocean-embed/docs/data-audit.json').write_text(json.dumps(findings,indent=2,default=lambda x:x.item()))
print(json.dumps({k:v for k,v in findings.items() if k!='case_source_checks'},indent=2));print('Case matches:',all(x['glorys_matches_cube'] for x in findings['case_source_checks']),'Argo finite:',sum(x['argo_cube_finite'] for x in findings['case_source_checks']))
