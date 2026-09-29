/** Protocol fixture only. The delivery bundle's cross-repo suite tests the real backend. */
import { createServer } from 'node:http';
import { promises as fs } from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import { makeRecord } from '../../../skills/project/scripts/transport.mjs';
export async function harness() {
  const temp = await fs.realpath(await fs.mkdtemp(path.join(os.tmpdir(), 'project-native-test-')));
  const readKey = 'b'.repeat(43); let record, revoked=false;
  const server=createServer((request,response)=>{
    if(request.headers.authorization!=='Bearer '+readKey) { response.writeHead(401);response.end();return; }
    if(!record||request.url!=='/api/handoffs/'+record.id) { response.writeHead(404);response.end();return; }
    if(revoked) { response.writeHead(410);response.end();return; }
    response.writeHead(200,{'Content-Type':'application/json'});response.end(JSON.stringify({record,expiresAt:Date.now()+60000}));
  });
  await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
  const origin='http://127.0.0.1:'+server.address().port,config=path.join(temp,'connector.json');
  await fs.writeFile(config,JSON.stringify({origin,readKey}),{mode:0o600});
  return {config,readKey,store:{publish:async bundle=>{record=await makeRecord(bundle);return {record};},revoke:async()=>{revoked=true;}},close:async()=>{server.closeAllConnections();await new Promise(resolve=>server.close(resolve));await fs.rm(temp,{recursive:true,force:true});}};
}
