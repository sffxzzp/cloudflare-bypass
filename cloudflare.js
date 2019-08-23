var targetUrl = 'https://steamdb.info/sub/334127';
var urlLen = targetUrl.replace('http://', '').replace('https://', '').split('/')[0].length;
var vName = /s,t,o,p,b,r,e,a,k,i,n,g,f, (.*)=\{"(.*)":(.*)};/.exec(res);
var fName = vName[1];
var sName = vName[2];
var fCode = eval(vName[3]);
var sCode = /;.*121'/.exec(res)[0];
sCode = sCode.split(';');
for (var i=1;i<sCode.length-3;i++) {
    eval(sCode[i].replace(fName+'.'+sName, 'fCode'));
}
var postPath = 'https://steamdb.info' + /form id="challenge-form" action="(.*?)"/.exec(res)[1];
var s = /input type="hidden" name="s" value="(.*?)"/.exec(res)[1];
s = encodeURIComponent(s);
var jschl_vc = /input type="hidden" name="jschl_vc" value="(.*?)"/.exec(res)[1];
var pass = /input type="hidden" name="pass" value="(.*?)"/.exec(res)[1];
var answer = (+fCode+urlLen).toFixed(10);
jQuery.ajax({
    url: postPath+'?s='+s+'&jschl_vc='+jschl_vc+'&pass='+pass+'&jschl_answer='+answer,
    method: 'get',
    onload: console.log,
    onerror: console.log,
    ontimeout: console.log
});
