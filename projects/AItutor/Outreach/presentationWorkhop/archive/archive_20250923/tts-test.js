#!/usr/bin/env node
/**
 * Simple TTS test helper
 * Usage:
 *   Local proxy (server must be running on PORT or 3000):
 *     node tts-test.js --text "Hello world from local" --local
 *   Direct Azure (bypasses local server):
 *     AZURE_SPEECH_KEY=... AZURE_SPEECH_REGION=eastus node tts-test.js --text "Direct call" --direct
 * Options:
 *   --voice en-US-JennyNeural (default)
 *   --format audio-24khz-48kbitrate-mono-mp3 (default)
 *   --out custom.mp3 (output filename)
 */

const fs = require('fs');
const path = require('path');

async function main(){
  const args = process.argv.slice(2);
  const get = (flag, def=null)=>{const i=args.indexOf(flag);return i>=0?args[i+1]:def;};
  const has = (flag)=>args.includes(flag);
  const text = get('--text', 'Hello Azure speech test');
  const voice = get('--voice','en-US-JennyNeural');
  const format = get('--format','audio-24khz-48kbitrate-mono-mp3');
  const outFile = get('--out','tts-test-output.mp3');
  const useLocal = has('--local');
  const useDirect = has('--direct');

  if(useLocal && useDirect){
    console.error('Choose only one of --local or --direct');
    process.exit(1);
  }

  if(!useLocal && !useDirect){
    console.log('No mode specified, defaulting to --local');
  }

  const start = Date.now();
  try {
    let audioBuffer;
    if(useDirect){
      const key = process.env.AZURE_SPEECH_KEY;
      const region = process.env.AZURE_SPEECH_REGION;
      if(!key || !region){
        console.error('Missing AZURE_SPEECH_KEY or AZURE_SPEECH_REGION');
        process.exit(1);
      }
      const tokenResp = await fetch(`https://${region}.api.cognitive.microsoft.com/sts/v1.0/issueToken`, {method:'POST', headers:{'Ocp-Apim-Subscription-Key': key}});
      if(!tokenResp.ok){
        throw new Error('Token request failed '+tokenResp.status);
      }
      const token = await tokenResp.text();
      const ssml = `<?xml version="1.0" encoding="utf-8"?>\n<speak version="1.0" xml:lang="en-US"><voice name="${voice}">${text.replace(/&/g,'&amp;')}</voice></speak>`;
      const ttsResp = await fetch(`https://${region}.tts.speech.microsoft.com/cognitiveservices/v1`, {method:'POST', headers:{'Authorization':`Bearer ${token}`,'Content-Type':'application/ssml+xml','X-Microsoft-OutputFormat':format,'User-Agent':'TTS-CLI-Test'}, body:ssml});
      if(!ttsResp.ok){
        const errTxt = await ttsResp.text();
        throw new Error('Azure TTS failed '+ttsResp.status+' '+errTxt.slice(0,200));
      }
      audioBuffer = Buffer.from(await ttsResp.arrayBuffer());
    } else {
      // local proxy
      const port = process.env.PORT || 3000;
      const resp = await fetch(`http://localhost:${port}/api/tts`, {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({text, voice, format})});
      if(!resp.ok){
        const err = await resp.text();
        throw new Error('Local /api/tts failed '+resp.status+' '+err.slice(0,200));
      }
      audioBuffer = Buffer.from(await resp.arrayBuffer());
    }

    if(audioBuffer.length < 500){
      console.warn('Warning: very small audio file ('+audioBuffer.length+' bytes)');
    }

    fs.writeFileSync(path.resolve(outFile), audioBuffer);
    const ms = Date.now()-start;
    console.log('✅ Saved', outFile, '| size:', audioBuffer.length, 'bytes | time:', ms+'ms');
  } catch (e) {
    console.error('❌ TTS test failed:', e.message);
    process.exit(1);
  }
}

main();
