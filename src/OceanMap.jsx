import { useEffect, useMemo } from 'react';
import { MapContainer, TileLayer, CircleMarker, Popup, useMap, useMapEvents, Rectangle } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
function Events({onSelect}) { useMapEvents({click:e=>onSelect(e.latlng.lat,e.latlng.lng)});return null; }
function Coverage({points}){
 const map=useMap();
 useEffect(()=>{const renderer=L.canvas({padding:0.2});const group=L.layerGroup(points.map(p=>L.circleMarker(p,{renderer,radius:1.5,stroke:false,fillColor:'#38bdf8',fillOpacity:0.5,interactive:false}))).addTo(map);return()=>group.remove();},[map,points]);
 useEffect(()=>{const t=setTimeout(()=>map.invalidateSize(),100);return()=>clearTimeout(t);},[map]);
 return null;
}
export default function OceanMap({points=[],lat,lon,onSelect,region='all'}){
 const visible=useMemo(()=>points.filter(p=>region==='all'||(p[1]>=78?'bay_of_bengal':'arabian_sea')===region),[points,region]);
 return <MapContainer center={[16,77]} zoom={4} minZoom={3} maxZoom={10} style={{height:'100%',width:'100%',background:'#0f2740'}}>
  <TileLayer url="https://server.arcgisonline.com/ArcGIS/rest/services/Ocean/World_Ocean_Base/MapServer/tile/{z}/{y}/{x}" attribution="Tiles © Esri — GEBCO, NOAA, National Geographic, DeLorme" />
  <Rectangle bounds={[[5,45],[30,105]]} pathOptions={{color:'#005A9C',weight:1,fill:false}}/>
  <Coverage points={visible}/><Events onSelect={onSelect}/>
  {Number.isFinite(Number(lat))&&Number.isFinite(Number(lon))&&<CircleMarker center={[Number(lat),Number(lon)]} radius={7} pathOptions={{color:'#fff',fillColor:'#FF9933',fillOpacity:1,weight:2}}><Popup>Requested location<br/>{Number(lat).toFixed(3)}°N, {Number(lon).toFixed(3)}°E</Popup></CircleMarker>}
 </MapContainer>;
}
