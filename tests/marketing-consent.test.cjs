// Run the real consent loader against a small fake DOM and mocked vendor scripts.
// No real browser, network requests, or tracking accounts are used.
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const source = fs.readFileSync('static/js/marketing-consent.js', 'utf8');
const key = 'digicode.marketing-consent.v1';
const duration = 180 * 24 * 60 * 60 * 1000;
const script = (text, attributes = {}) => ({attributes, text});
const config = {fingerprint:'version-a',snippets:[{position:'head',scripts:[script('window.runs = (window.runs || 0) + 1;')]},{position:'body_start',scripts:[script('window.bodyRuns = (window.bodyRuns || 0) + 1;')]}]};
const settle = () => new Promise(resolve => setTimeout(resolve, 25));

function environment(configuration=config, stored=null, storageFailure=false) {
  const records=[];
  const data=new Map(stored ? [[key, JSON.stringify(stored)]] : []);
  const button = value => ({dataset:{marketingChoice:value},events:{},addEventListener(type,callback){this.events[type]=callback;},click(){this.events.click();},focus(){this.focused=true;}});
  const accept=button('accepted'),reject=button('rejected'),preferences=button();
  preferences.hidden=true;
  const banner={hidden:true,querySelectorAll:()=>[accept,reject],querySelector:()=>accept};
  const marker={nodeType:8,textContent:'digicode-marketing-body-start'};
  const state={records,accept,reject,preferences,banner,data,reloads:0};
  const context={console,Date,Number,Object,JSON,Array,Promise,clearTimeout,setTimeout:(fn,ms)=>setTimeout(fn,Math.min(ms,5))};
  context.window=context;
  context.localStorage={getItem(k){if(storageFailure)throw Error('blocked');return data.get(k)||null;},setItem(k,v){if(storageFailure)throw Error('blocked');data.set(k,v);}};
  context.location={reload(){state.reloads++;}};
  function append(node,position){
    records.push({position,attrs:node.attributes,text:node.textContent,async:node.async});
    if(node.attributes.src){
      if(node.attributes.src.includes('stall')) return;
      setImmediate(()=>{
        if(node.attributes.src.includes('failure')) node.onerror?.();
        else { context.vendorLoaded=true;node.onload?.(); }
      });
    }else{
      try{vm.runInContext(node.textContent,context);}catch{/* Browser errors don't stop independent snippets. */}
      if(node.attributes.type==='module')setImmediate(()=>node.onload?.());
    }
  }
  context.document={
    getElementById(id){return id==='marketing-config' ? (configuration ? {textContent:JSON.stringify(configuration)}:null):banner;},
    querySelector:()=>preferences,
    createElement(){return {attributes:{},async:true,setAttribute(k,v){this.attributes[k]=v;}};},
    head:{appendChild(node){append(node,'head');}},
    body:{childNodes:[marker],firstChild:marker,insertBefore(node,anchor){assert.equal(anchor,marker);append(node,'body_start');}},
  };
  vm.createContext(context);vm.runInContext(source,context);
  return {...state,context,state};
}
const saved = (choice='accepted', fingerprint='version-a', expires=Date.now()+duration) => ({choice,fingerprint,expires});

test('unknown choice loads no vendor code; reject remains unloaded',async()=>{
  const env=environment();assert.equal(env.records.length,0);assert.equal(env.banner.hidden,false);
  env.reject.click();await settle();assert.equal(env.records.length,0);assert.equal(env.banner.hidden,true);
  assert.equal(JSON.parse(env.data.get(key)).choice,'rejected');
});
test('accept executes once in the correct positions, even when accepted twice',async()=>{
  const env=environment();env.accept.click();await settle();env.accept.click();await settle();
  assert.equal(env.context.runs,1);assert.equal(env.context.bodyRuns,1);
  assert.deepEqual(env.records.map(record=>record.position),['head','body_start']);
});
test('matching stored acceptance loads, stored rejection does not',async()=>{
  const accepted=environment(config,saved());await settle();assert.equal(accepted.context.runs,1);assert.equal(accepted.banner.hidden,true);
  const rejected=environment(config,saved('rejected'));await settle();assert.equal(rejected.records.length,0);assert.equal(rejected.banner.hidden,true);
});
test('expired, changed, invalid and implausible preferences fail closed',async()=>{
  for(const stored of [saved('accepted','other'),saved('accepted','version-a',Date.now()-1),saved('broken'),saved('accepted','version-a','tomorrow'),saved('accepted','version-a',Date.now()+duration*2)]){
    const env=environment(config,stored);await settle();assert.equal(env.records.length,0);assert.equal(env.banner.hidden,false);
  }
});
test('unavailable storage only honors an explicit current-page choice',async()=>{
  const env=environment(config,null,true);assert.equal(env.records.length,0);env.accept.click();await settle();assert.equal(env.context.runs,1);
  const nextPage=environment(config,null,true);assert.equal(nextPage.records.length,0);assert.equal(nextPage.banner.hidden,false);
});
test('withdrawal stops tracking and reloads; next page stays rejected',async()=>{
  const env=environment();env.accept.click();await settle();env.preferences.click();assert.equal(env.banner.hidden,false);assert.equal(env.accept.focused,true);
  env.reject.click();assert.equal(env.state.reloads,1);assert.equal(env.preferences.focused,true);
  const nextPage=environment(config,JSON.parse(env.data.get(key)));await settle();assert.equal(nextPage.records.length,0);
});
test('external synchronous scripts finish before their dependent initialization',async()=>{
  const conf={fingerprint:'version-a',snippets:[{position:'head',scripts:[script('',{src:'https://mock.test/vendor.js',integrity:'test',crossorigin:'anonymous'}),script('window.dependencyWasReady = window.vendorLoaded;')]}]};
  const env=environment(conf);env.accept.click();await settle();assert.equal(env.context.dependencyWasReady,true);assert.equal(env.records[0].async,false);assert.equal(env.records[0].attrs.integrity,'test');
});
test('explicit async is preserved; inline queue initialization proceeds',async()=>{
  const conf={fingerprint:'version-a',snippets:[{position:'head',scripts:[script('',{src:'https://mock.test/gtag.js',async:null}),script('window.dataLayer=[];function gtag(){dataLayer.push(arguments)}gtag("config","G-TEST");')]}]};
  const env=environment(conf);env.accept.click();await settle();assert.equal(env.records[0].async,true);assert.equal(env.context.dataLayer.length,1);
});
test('failed and stalled vendors do not block subsequent snippets',async()=>{
  for(const type of ['failure','stall']){
    const conf={fingerprint:'version-a',snippets:[{position:'head',scripts:[script('',{src:`https://mock.test/${type}.js`})]},{position:'head',scripts:[script('window.independent = true;')]}]};
    const env=environment(conf);env.accept.click();await settle();assert.equal(env.context.independent,true);assert.equal(env.records.length,2);
  }
});
test('Meta-style inline setup and module scripts both execute',async()=>{
  const conf={fingerprint:'version-a',snippets:[{position:'head',scripts:[script('!function(f){f.fbq=function(){f.metaCalls=(f.metaCalls||0)+1;};}(window);fbq("init","TEST");'),script('window.moduleReady=true;',{type:'module'})]}]};
  const env=environment(conf);env.accept.click();await settle();assert.equal(env.context.metaCalls,1);assert.equal(env.context.moduleReady,true);
});
test('missing payload or an empty-script fallback creates no vendor requests',async()=>{
  const excluded=environment(null);await settle();assert.equal(excluded.records.length,0);
  const fallback=environment({fingerprint:'version-a',snippets:[{position:'body_start',scripts:[]}]});fallback.accept.click();await settle();assert.equal(fallback.records.length,0);
});
