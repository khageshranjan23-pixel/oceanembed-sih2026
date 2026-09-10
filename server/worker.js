import {api} from './api.js';
import indexHtml from '../dist/client/index.html' with {type:'text'};
export default {async fetch(request,env){const path=new URL(request.url).pathname;if(path==='/health'||path.startsWith('/api/'))return api(request,env);if(path==='/'||!path.split('/').pop().includes('.'))return new Response(indexHtml,{headers:{'content-type':'text/html; charset=utf-8','cache-control':'no-cache','x-content-type-options':'nosniff','referrer-policy':'strict-origin-when-cross-origin'}});return new Response('Not found',{status:404});}};
