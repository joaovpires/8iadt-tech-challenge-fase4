// Gera uma serie temporal sintetica de sinais vitais de um paciente,
// com anomalias injetadas de proposito (para testar a deteccao de anomalias).
// Uso: node gerar_vitais.js  ->  gera vitais_simulados.csv
const fs = require('fs');

const N = 720;                 // 720 leituras (ex: 1 a cada 1 min = 12h)
const startTs = new Date('2026-07-21T08:00:00');
function gauss(mean, sd) {     // Box-Muller
  const u = 1 - Math.random(), v = Math.random();
  return mean + sd * Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v);
}

// Janelas de anomalia: [inicio, fim, tipo]
const anomalias = [
  [180, 195, 'taquicardia'],     // HR sobe muito
  [400, 410, 'hipoxia'],         // SpO2 despenca
  [600, 615, 'hipertensao'],     // Pressao sobe
];
function anomAtiva(i, tipo){ return anomalias.some(([a,b,t]) => t===tipo && i>=a && i<=b); }

const rows = [['timestamp','heart_rate','spo2','systolic_bp','diastolic_bp','temperature','resp_rate','anomalia_esperada']];
for (let i = 0; i < N; i++) {
  const ts = new Date(startTs.getTime() + i * 60000).toISOString();
  let hr   = gauss(75, 4);
  let spo2 = gauss(98, 0.6);
  let sys  = gauss(118, 5);
  let dia  = gauss(78, 4);
  let temp = gauss(36.6, 0.15);
  let rr   = gauss(15, 1.2);
  let flag = 0;
  if (anomAtiva(i,'taquicardia')) { hr = gauss(145, 6); rr = gauss(24, 1.5); flag = 1; }
  if (anomAtiva(i,'hipoxia'))     { spo2 = gauss(86, 1.5); hr = gauss(105, 5); flag = 1; }
  if (anomAtiva(i,'hipertensao')) { sys = gauss(165, 6); dia = gauss(102, 4); flag = 1; }
  rows.push([ts, hr.toFixed(1), spo2.toFixed(1), sys.toFixed(0), dia.toFixed(0), temp.toFixed(2), rr.toFixed(1), flag]);
}
fs.writeFileSync(require('path').join(__dirname, 'vitais_simulados.csv'), rows.map(r => r.join(',')).join('\n') + '\n');
console.log(`OK: vitais_simulados.csv gerado com ${N} linhas e ${anomalias.length} janelas de anomalia.`);
