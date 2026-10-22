import fs from 'node:fs';
import path from 'node:path';
import { execSync } from 'node:child_process';
import sharp from 'sharp';

const inventoryPath = '/home/civo/.gemini/antigravity-cli/brain/ccde7d57-ec12-4900-82ae-6e883d74e386/scratch/media_inventory.json';
const inventory = JSON.parse(fs.readFileSync(inventoryPath, 'utf8'));

function getToken() {
  return execSync('gcloud auth print-access-token', { encoding: 'utf8' }).trim();
}

let token = getToken();

async function downloadFile(id, destPath, retries = 2) {
  if (fs.existsSync(destPath)) {
    const stats = fs.statSync(destPath);
    if (stats.size > 10000) {
      console.log(`[SKIP] Already exists: ${destPath}`);
      return;
    }
  }

  for (let attempt = 1; attempt <= retries; attempt++) {
    try {
      const url = `https://www.googleapis.com/drive/v3/files/${id}?alt=media`;
      const res = await fetch(url, {
        headers: { Authorization: `Bearer ${token}` }
      });

      if (res.status === 401) {
        console.log('Refreshing token...');
        token = getToken();
        continue;
      }

      if (!res.ok) {
        throw new Error(`HTTP ${res.status}: ${res.statusText}`);
      }

      const arrayBuffer = await res.arrayBuffer();
      const inputBuffer = Buffer.from(arrayBuffer);

      // Process with sharp
      fs.mkdirSync(path.dirname(destPath), { recursive: true });
      await sharp(inputBuffer)
        .rotate() // auto-orient based on EXIF
        .resize({ width: 2400, height: 2400, fit: 'inside', withoutEnlargement: true })
        .webp({ quality: 88, effort: 4 })
        .toFile(destPath);

      const outStat = fs.statSync(destPath);
      console.log(`[SAVED] ${destPath} (${Math.round(outStat.size / 1024)} KB)`);
      return;
    } catch (err) {
      console.error(`[ERROR] Attempt ${attempt} failed for ${id}: ${err.message}`);
      if (attempt === retries) throw err;
      await new Promise(r => setTimeout(r, 1000));
    }
  }
}

const PROJECT_CONFIGS = [
  {
    slug: 'bangalo-60-carneiros',
    folder: 'Silvio/Fotos/Bangalô 60',
    files: [
      { name: '2021.11.06_BANGALÔ 01_ALTA_05.jpg', out: '01-cover.webp' },
      { name: '2021.11.06_BANGALÔ 01_ALTA_01.jpg', out: '02-estar-terraco.webp' },
      { name: '2021.11.06_BANGALÔ 01_ALTA_12.jpg', out: '03-marcenaria-detalhe.webp' },
      { name: '2021.11.06_BANGALÔ 01_ALTA_13.jpg', out: '04-painel-madeira.webp' },
      { name: '2021.11.06_BANGALÔ 01_ALTA_08.jpg', out: '05-jantar-deck.webp' },
      { name: '2021.11.06_BANGALÔ 01_ALTA_14.jpg', out: '06-suite-luz.webp' },
      { name: '2021.11.06_BANGALÔ 01_ALTA_32.jpg', out: '07-banheiro-pedra.webp' },
      { name: '2021.11.06_BANGALÔ 01_ALTA_48.jpg', out: '08-piscina-crepusculo.webp' },
    ]
  },
  {
    slug: 'bangalo-48-carneiros',
    folder: 'Silvio/Fotos/Bangalô 48',
    files: [
      { name: '2021.10.06_TRÓPIKOS_ALTA_01.jpg', out: '01-cover.webp' },
      { name: '2021.10.06_TRÓPIKOS_ALTA_04.jpg', out: '02-estar-integrado.webp' },
      { name: '2021.10.06_TRÓPIKOS_ALTA_03.jpg', out: '03-brise-madeira.webp' },
      { name: '2021.10.06_TRÓPIKOS_ALTA_06.jpg', out: '04-sombras-verticais.webp' },
      { name: '2021.10.06_TRÓPIKOS_ALTA_07.jpg', out: '05-suite-aberta.webp' },
      { name: '2021.10.06_TRÓPIKOS_ALTA_09.jpg', out: '06-texturas-linho.webp' },
      { name: '2021.10.06_TRÓPIKOS_ALTA_11.jpg', out: '07-banheiro-jardim.webp' },
      { name: '2021.10.06_TRÓPIKOS_ALTA_27.jpg', out: '08-deck-privativo.webp' },
    ]
  },
  {
    slug: 'casa-gravata',
    folder: 'Silvio/Fotos/Casa no centro de Gravatá',
    files: [
      { name: 'WALTER DIAS_2021.11.17_TROPIKOS_ALTA_15.jpg', out: '01-cover.webp' },
      { name: 'WALTER DIAS_2021.11.17_TROPIKOS_ALTA_03.jpg', out: '02-pavilhao-estar.webp' },
      { name: 'WALTER DIAS_2021.11.17_TROPIKOS_ALTA_01.jpg', out: '03-colunas-madeira.webp' },
      { name: 'WALTER DIAS_2021.11.17_TROPIKOS_ALTA_02.jpg', out: '04-luz-serrana.webp' },
      { name: 'WALTER DIAS_2021.11.17_TROPIKOS_ALTA_23.jpg', out: '05-lareira-cozinha.webp' },
      { name: 'WALTER DIAS_2021.11.17_TROPIKOS_ALTA_11.jpg', out: '06-varanda-suite.webp' },
      { name: 'WALTER DIAS_2021.11.17_TROPIKOS_ALTA_12.jpg', out: '07-banco-pedra.webp' },
      { name: 'WALTER DIAS_2021.11.17_TROPIKOS_ALTA_37.jpg', out: '08-piscina-noturna.webp' },
    ]
  },
  {
    slug: 'apartamento-rosarinho',
    folder: 'Edjane Figueiredo - Apto Rosarinho/Fotos oficiais',
    files: [
      { name: 'IMG_9519-1.jpg', out: '01-cover.webp' },
      { name: 'IMG_9522-2.jpg', out: '02-estar-aparador.webp' },
      { name: 'IMG_9858-35.jpg', out: '03-mesa-pendente.webp' },
      { name: 'IMG_9895-42.jpg', out: '04-portal-marcenaria.webp' },
      { name: 'IMG_9549-3.jpg', out: '05-bancada-gourmet.webp' },
      { name: 'IMG_9767-15.jpg', out: '06-suite-cabeceira.webp' },
      { name: 'IMG_9845-32.jpg', out: '07-lavabo-concreto.webp' },
      { name: 'IMG_9873-39.jpg', out: '08-iluminacao-natural.webp' },
    ]
  },
  {
    slug: 'casa-brut',
    folder: 'Casa BRUT',
    files: [
      { name: 'Fachada frontal final_12.jpg', out: '01-cover.webp' },
      { name: 'Fachada frontal final_4.jpg', out: '02-fachada-poente.webp' },
      { name: 'Fachada extra 1.jpg', out: '03-volume-suspenso.webp' },
      { name: 'Sala jantar e cozinha final_1 - Photo.jpg', out: '04-cozinha-ilha.webp' },
      { name: 'Estar final_19 - Foto.jpg', out: '05-pe-direito-duplo.webp' },
      { name: 'Área externa final_8 - Photo.jpg', out: '06-piscina-concreto.webp' },
      { name: 'Área externa final_3 - Photo.jpg', out: '07-escada-flutuante.webp' },
      { name: 'Fachada frontal final_7.jpg', out: '08-acesso-pedestre.webp' },
    ]
  },
  {
    slug: 'casa-ipubi',
    folder: 'Casa Ipubi',
    files: [
      { name: 'Externas 03 final_5 - Photo.jpg', out: '01-cover.webp' },
      { name: 'Externas 01 final_3 - Photo.jpg', out: '02-acesso-principal.webp' },
      { name: 'Salas e Hall final_15 - Foto.jpg', out: '03-living-ventilacao.webp' },
      { name: '6.jpg', out: '04-detalhe-cobogo.webp' },
      { name: 'Espeço gourmet final_7 - Photo.jpg', out: '05-espaco-gourmet.webp' },
      { name: 'Salas e Hall final_20 - Foto.jpg', out: '06-jardim-interno.webp' },
      { name: 'Externas 02 final_2 - Photo.jpg', out: '07-crepusculo-cobogo.webp' },
    ]
  },
  {
    slug: 'apartamento-graca',
    folder: 'Edjane Figueiredo - Apto Graças',
    files: [
      { name: 'Apto graças final_37 - Foto.jpg', out: '01-cover.webp' },
      { name: 'Apto graças final_36 - Foto.jpg', out: '02-cozinha-ilha.webp' },
      { name: 'Apto graças final_32 - Foto.jpg', out: '03-painel-ripado.webp' },
      { name: 'Apto graças final_33 - Foto.jpg', out: '04-luminaria-tecido.webp' },
      { name: 'Apto graças final_35 - Foto.jpg', out: '05-estante-livros.webp' },
      { name: 'Apto graças final_25 - Foto.jpg', out: '06-suite-casal.webp' },
      { name: 'Apto graças final_22 - Foto.jpg', out: '07-varanda-copa.webp' },
    ]
  },
  {
    slug: 'clinica-esthetica',
    folder: 'Clínica Esthetica',
    files: [
      { name: 'IMG_0969.JPEG', out: '01-cover.webp' },
      { name: 'IMG_0973.JPEG', out: '02-consultorio-luz.webp' },
      { name: 'IMG_0976.JPEG', out: '03-recepcao-ripado.webp' },
      { name: 'IMG_0978.JPEG', out: '04-espelho-led.webp' },
      { name: 'IMG_0980.JPEG', out: '05-sala-procedimento.webp' },
      { name: 'IMG_1002.JPEG', out: '06-lounge-espera.webp' },
      { name: 'IMG_0994.JPEG', out: '07-corredor-iluminacao.webp' },
    ]
  },
  {
    slug: 'casas-geminadas-condominio',
    folder: 'Bruno Caffé Casas geminadas em condomínio',
    files: [
      { name: 'Fachada final_12 - Photo.jpg', out: '01-cover.webp' },
      { name: 'Fachada final_4 - Photo.jpg', out: '02-pergola-garagem.webp' },
      { name: 'Cozinha final_15 - Foto.jpg', out: '03-cozinha-jantar.webp' },
      { name: 'Salas final_9 - Photo.jpg', out: '04-estar-vidro.webp' },
      { name: 'Piscina e gourmet final_4 - Photo.jpg', out: '05-piscina-lazer.webp' },
      { name: 'Fachada final_7 - Photo.jpg', out: '06-fachada-noturna.webp' },
      { name: 'Cozinha final_13 - Foto.jpg', out: '07-detalhe-marcenaria.webp' },
    ]
  },
  {
    slug: 'studio',
    folder: 'Edjane Figueiredo - Apto Rosarinho/Shooting - Nati',
    destDir: 'src/assets/studio',
    files: [
      { name: 'IMG_6120.JPG', out: '01-estudio-espaco.webp' },
      { name: 'IMG_E6119.JPG', out: '02-estudio-processo.webp' },
      { name: 'IMG_6118.JPG', out: '03-estudio-colaboracao.webp' },
    ]
  }
];

async function run() {
  console.log('Starting Google Drive portfolio assets sync...');
  let totalDownloaded = 0;

  for (const proj of PROJECT_CONFIGS) {
    const destDir = proj.destDir || `src/assets/projects/${proj.slug}`;
    console.log(`\n=== Processing: ${proj.slug} -> ${destDir} ===`);

    for (const item of proj.files) {
      const match = inventory.media.find(m => m.folder_path.includes(proj.folder) && m.name === item.name);
      if (!match) {
        console.error(`[ERROR] File not found in inventory: ${proj.folder} / ${item.name}`);
        continue;
      }

      const destPath = path.join(destDir, item.out);
      await downloadFile(match.id, destPath);
      totalDownloaded++;
    }
  }

  console.log(`\nSync complete! Processed ${totalDownloaded} media assets.`);
}

run().catch(err => {
  console.error('Fatal error during sync:', err);
  process.exit(1);
});
