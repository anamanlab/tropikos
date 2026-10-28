// Single source of truth for copy, contact details and navigation.
export const SITE = {
  name: 'Trópikos Arquitetos',
  shortName: 'TRÓPIKOS',
  description:
    'Trópikos Arquitetos — escritório de arquitetura e interiores no Recife. Projetos autorais, execução e acompanhamento de obra do conceito à entrega.',
  city: 'Recife',
  state: 'PE',
  country: 'Brasil',
  address: {
    street: 'Rua Ferreira Lopes, 334',
    building: 'Salas 201/202/203',
    district: 'Parnamirim',
    city: 'Recife',
    state: 'PE',
    postalCode: '52060-235',
    country: 'BR',
  },
  email: 'tropikosarquitetura@gmail.com',
  phone: '+55 81 99302-0201',
  phoneAlt: '+55 81 99767-4444',
  whatsapp: '5581993020201',
  whatsappHref:
    'https://wa.me/5581993020201?text=' +
    encodeURIComponent('Olá, vim pelo site e gostaria de conversar sobre um projeto.'),
  instagram: 'https://www.instagram.com/tropikosarq/',
  instagramHandle: '@tropikosarq',
  linktree: 'https://linktr.ee/tropikosarq',
  founded: 2021,
  locale: 'pt-BR',
  timezone: 'America/Recife',
  timezoneAlt: 'Europe/Paris',
  cityCode: 'REC',
  cityCodeAlt: 'PAR',
} as const;

/** E.164 tel: href. Keeps the leading "+", which a \D strip would drop. */
export const telHref = (number: string) => `tel:${number.replace(/[\s()\-.]/g, '')}`;

/** WhatsApp link whose prefilled message names the place, so the studio can see where a lead came from. */
export const whatsappHrefFor = (message: string) =>
  `https://wa.me/${SITE.whatsapp}?text=${encodeURIComponent(message)}`;

export const NAV_LINKS = [
  { label: 'Projetos', href: '/projetos', index: '01' },
  { label: 'Estúdio', href: '/estudio', index: '02' },
  { label: 'Serviços', href: '/servicos', index: '03' },
  { label: 'Atuação', href: '/atuacao', index: '04' },
  { label: 'Contato', href: '/contato', index: '05' },
] as const;

export const SERVICES = [
  {
    index: '01',
    title: 'Projeto arquitetônico',
    body: 'Estudo do terreno, implantação, volumetria e detalhamento executivo. Cada decisão responde ao lugar, à luz e ao modo de morar.',
    items: ['Residencial', 'Interiores', 'Reformas', 'Uso misto'],
  },
  {
    index: '02',
    title: 'Interiores',
    body: 'Materiais, marcenaria, iluminação e mobiliário desenhados em conjunto com a arquitetura — sem ruído entre projeto e obra.',
    items: ['Layout', 'Marcenaria', 'Iluminação', 'Curadoria'],
  },
  {
    index: '03',
    title: 'Execução e obra',
    body: 'Orçamento, cronograma, compras e acompanhamento técnico. O desenho chega de pé à entrega, com responsabilidade sobre cada etapa.',
    items: ['Planejamento', 'Gestão', 'Fiscalização', 'Entrega'],
  },
  {
    index: '04',
    title: 'Consultoria',
    body: 'Leituras pontuais de projeto, obra em andamento ou potencial de um imóvel, com parecer técnico objetivo e próximo.',
    items: ['Diagnóstico', 'Viabilidade', 'Parecer', 'Diretrizes'],
  },
] as const;

/**
 * Service areas are cities the studio takes on work in — not offices. Each page
 * names the Recife base in its own words, explains how visits happen, and ties
 * the local content to real landmarks and real design consequences. `projects`
 * lists real portfolio ids; the build fails on an id that is missing or draft,
 * and every card prints its own status and location.
 */
export type ServiceArea = {
  slug: string;
  city: string;
  region: string;
  metaTitle: string;
  metaDescription: string;
  h1: string;
  standfirst: string;
  /** One-line local hook for the hub list. */
  hubNote: string;
  intro: string[];
  /** A landmark or local condition, and what it changes in the project. */
  localLens: { place: string; body: string }[];
  /** Prose answer to "what does the studio take on in this city?". */
  whereWeWork: string;
  /** How visits and travel are arranged for this city. */
  attendance: string;
  faq: { question: string; answer: string }[];
  projectsNote: string;
  projects: string[];
};

export const SERVICE_MODEL = {
  heading: 'Como atendemos fora do Recife',
  paragraphs: [
    'O estúdio tem sede no Recife, no Parnamirim, e desenvolve projetos de arquitetura, interiores e reformas em outras cidades de Pernambuco. O grosso do trabalho — escuta, estudos, reuniões, detalhamento e entrega de documentos — acontece à distância, com o mesmo processo usado na capital.',
    'O que exige presença acontece sob agendamento: levantamento e medição do imóvel, vistorias em momentos-chave da obra e a entrega. A quantidade dessas visitas é definida no escopo, junto com o custo de deslocamento, antes da contratação. Nada aparece depois como surpresa.',
    'Cada cidade pede um cuidado diferente. Antes de desenhar, verificamos as normas que valem para o endereço específico, o clima, a forma de construir local e o uso real que o imóvel vai ter. O que não fazemos é transportar um modelo pronto de um lugar para o outro.',
  ],
  steps: [
    {
      index: '01',
      title: 'Conversa e endereço',
      body: 'Você envia a localização, fotos e o que precisa mudar. Dizemos se o estúdio atende aquele caso e o que ele exige.',
    },
    {
      index: '02',
      title: 'Levantamento in loco',
      body: 'Visita técnica agendada para medir, ler a construção existente e entender entorno, solar e ventilação.',
    },
    {
      index: '03',
      title: 'Projeto à distância',
      body: 'Estudos e executivo desenvolvidos no Recife, com reuniões por videochamada e entregas documentadas.',
    },
    {
      index: '04',
      title: 'Obra com presença programada',
      body: 'Vistorias nos marcos que decidem o resultado, definidas no escopo — não improvisadas no meio do caminho.',
    },
  ],
} as const;

export const SERVICE_AREAS: ServiceArea[] = [
  {
    slug: 'olinda',
    city: 'Olinda',
    region: 'Região Metropolitana do Recife',
    metaTitle: 'Arquiteto em Olinda',
    metaDescription:
      'Arquitetura, interiores e reformas em Olinda, do Sítio Histórico à orla de Casa Caiada. Estúdio no Recife, com visitas combinadas e deslocamento no escopo.',
    h1: 'Arquitetura em Olinda, entre a ladeira e a maré.',
    standfirst:
      'Projetos de arquitetura, interiores e reformas para casas e apartamentos em Olinda, feitos a partir do Recife.',
    hubNote: 'Do Sítio Histórico à orla de Casa Caiada: ladeira, maresia e prédio antigo.',
    intro: [
      'Olinda não é um lugar só. Quem sobe ao Sítio Histórico encontra casario colonial, rua estreita e vista aberta para o mar. Quem mora em Casa Caiada ou Bairro Novo está em outra cidade: prédio de orla, lote regular, vida de bairro. São dois modos de morar no mesmo município — e dois conjuntos de decisões de projeto.',
      'O estúdio fica no Recife, no Parnamirim. As visitas a Olinda são agendadas: levantamento, vistorias e entrega acontecem em dias combinados, e o deslocamento entra no escopo desde o orçamento.',
      'A distância é curta. O que muda é a pergunta que cada endereço faz. Apartamento em Casa Caiada pede ventilação, proteção solar e material que aguente maresia; casa no Sítio Histórico pede a leitura das normas de preservação antes de qualquer traço.',
    ],
    localLens: [
      {
        place: 'As ladeiras do Alto da Sé',
        body: 'Rua estreita, muro de arrimo e vista que abre de repente. Casa em ladeira se resolve por níveis: onde entra o carro, onde fica a varanda, onde o quarto recebe o vento. Errar a cota de implantação é errar a casa inteira.',
      },
      {
        place: 'O Sítio Histórico e o tombamento',
        body: 'A área é protegida e parte das intervenções passa por análise de órgãos de preservação. Antes de propor fachada ou ampliação, verificamos o que a norma permite naquele lote, para o desenho nascer aprovável.',
      },
      {
        place: 'A orla de Casa Caiada e Bairro Novo',
        body: 'Prédios dos anos 80 e 90, muitos com planta compartimentada e pouca abertura para o mar. Reorganizar cozinha, sala e varanda costuma render mais conforto do que qualquer acréscimo de área.',
      },
      {
        place: 'O Carnaval e o resto do ano',
        body: 'Em fevereiro o centro histórico muda de função. Casa que recebe gente, aluga temporada ou vira ponto de apoio precisa de circuito elétrico, banheiro e circulação pensados para esse pico.',
      },
    ],
    whereWeWork:
      'Em Olinda, o atendimento se organiza por tipo de imóvel. Na orla — Casa Caiada, Bairro Novo e Jardim Atlântico — são apartamentos e casas em prédios dos anos 80 e 90, onde maresia, insolação e planta compartimentada pesam no estudo. No Sítio Histórico, é o casario protegido: a intervenção começa pela leitura do que a norma permite no lote. Em Guadalupe e Rio Doce, a casa de esquina com uso misto e o apartamento antigo, em que reorganizar a planta rende mais que acrescentar metragem.',
    attendance:
      'Olinda está na Região Metropolitana, então levantamento e vistorias cabem em visitas de meio período. As datas são combinadas no início do projeto e o deslocamento entra no escopo.',
    faq: [
      {
        question: 'Vocês têm base em Olinda?',
        answer:
          'Não. A base é o Recife, no Parnamirim, e Olinda é atendida por visitas agendadas. O projeto é desenvolvido no Recife, com reuniões por vídeo e entregas documentadas a cada etapa.',
      },
      {
        question: 'Já entregaram projeto em Olinda?',
        answer:
          'Ainda não. Os projetos desta página foram feitos em outras cidades, e cada cartão mostra onde. O trabalho real está ali para você ver a linguagem do estúdio, não para sugerir uma obra que não existe.',
      },
      {
        question: 'Como funciona a visita ao imóvel?',
        answer:
          'O levantamento é agendado no início do projeto, e as vistorias seguem os marcos definidos no escopo. A quantidade de visitas e o deslocamento são combinados antes da contratação, sem custo que apareça depois.',
      },
      {
        question: 'O imóvel está no Sítio Histórico. Isso muda o projeto?',
        answer:
          'Muda a aprovação, não o cuidado. Verificamos a situação do lote junto aos órgãos de preservação antes de propor qualquer intervenção, para o projeto nascer compatível com o que a área protegida permite.',
      },
    ],
    projectsNote:
      'Ainda não executamos obra em Olinda. Os projetos abaixo são trabalho real do estúdio, e cada cartão indica a cidade e o estágio — construído ou projeto.',
    projects: ['apartamento-rosarinho', 'apartamento-gracas', 'bangalo-60-carneiros', 'casa-brut'],
  },
  {
    slug: 'jaboatao-dos-guararapes',
    city: 'Jaboatão dos Guararapes',
    region: 'Região Metropolitana do Recife',
    metaTitle: 'Arquiteto em Jaboatão dos Guararapes',
    metaDescription:
      'Arquitetura residencial, interiores e comércio em Jaboatão dos Guararapes, da orla de Piedade aos loteamentos. Visitas agendadas a partir do Recife.',
    h1: 'Arquitetura em Jaboatão, do lote à orla.',
    standfirst:
      'Projetos residenciais, de interiores e comerciais para quem mora ou investe em Jaboatão dos Guararapes.',
    hubNote: 'Piedade e Candeias de um lado, loteamento e comércio de avenida do outro.',
    intro: [
      'Jaboatão é comprida. De Jardim Petrópolis a Barra de Jangada são realidades que quase não se conversam: condomínio horizontal e casa térrea de um lado, avenida movimentada e prédio de orla do outro. O projeto começa por identificar em qual dessas cidades o imóvel está.',
      'O estúdio tem sede no Recife, no Parnamirim, e atende Jaboatão dos Guararapes com visitas marcadas. Levantamento, vistorias e entrega acontecem em dias combinados; o deslocamento é curto e entra no escopo desde o orçamento.',
      'Na faixa de Piedade, Candeias e Barra de Jangada, o mar está perto o bastante para pesar em fundação, esquadria e revestimento. No miolo do município, o desafio costuma ser outro: lote estreito, casa que cresceu sem projeto e a necessidade de reorganizar sem derrubar o que funciona.',
    ],
    localLens: [
      {
        place: 'Piedade, Candeias e Barra de Jangada',
        body: 'Solo arenoso, lençol alto e maresia no ar. Isso decide fundação, altura do piso e tipo de esquadria antes de qualquer escolha estética. Especificamos para o clima real do endereço.',
      },
      {
        place: 'O Jaboatão Antigo e o Morro',
        body: 'O Morro dos Guararapes e a Igreja de Nossa Senhora dos Prazeres guardam a parte mais antiga da cidade. Quem restaura ou amplia por ali lida com construção de outra época e precisa respeitar o que a estrutura e o entorno admitem.',
      },
      {
        place: 'Os loteamentos de Jardim Petrópolis e Curado',
        body: 'Lote padrão, casa repetida, fundos estreitos. Dá para ganhar luz e ventilação mexendo em circulação e aberturas, sem aumentar um metro quadrado de área construída.',
      },
      {
        place: 'O eixo da BR-101 e das avenidas',
        body: 'Loja, consultório e escritório em via de fluxo vivem de como as pessoas chegam e entram. Fachada, acessibilidade e posição da porta pesam mais que o acabamento interno.',
      },
    ],
    whereWeWork:
      'Em Jaboatão dos Guararapes, o atendimento segue o endereço. Na orla — Piedade, Candeias, Barra de Jangada — são casas e apartamentos com o mar perto, onde fundação, esquadria e revestimento entram cedo no estudo. No miolo residencial de Prazeres, Jardim Petrópolis e Curado, o foco é ampliação e reforma de interiores em loteamento. Na avenida, é o uso comercial de rua, do fluxo de entrada ao depósito nos fundos.',
    attendance:
      'As visitas a Jaboatão dos Guararapes são programadas por etapa e cabem em deslocamentos curtos a partir do Recife. Quantidade e custo entram no escopo, combinados antes de começar.',
    faq: [
      {
        question: 'Vocês têm base em Jaboatão dos Guararapes?',
        answer:
          'Não. A base é o Recife, no Parnamirim, e Jaboatão dos Guararapes é atendida com visitas agendadas. O desenvolvimento do projeto acontece no Recife, com reuniões por vídeo e entregas documentadas.',
      },
      {
        question: 'Já têm trabalho feito em Jaboatão?',
        answer:
          'Ainda não. Os projetos desta página estão em outras cidades, e cada cartão diz qual. A linguagem do estúdio é a mesma; o lugar é outro.',
      },
      {
        question: 'Dá para reformar apartamento sem mexer na estrutura?',
        answer:
          'Na maioria dos casos, sim. O levantamento in loco separa o que é estrutura do que é vedação, e é a partir dessa leitura que a reforma reorganiza planta e aberturas sem tocar no que sustenta o edifício.',
      },
      {
        question: 'Vocês entregam a documentação do condomínio?',
        answer:
          'O projeto já nasce compatível com o regulamento do condomínio, com as peças que a administração costuma exigir. Quando há exigência específica, ela entra no escopo antes de começar.',
      },
    ],
    projectsNote:
      'Não temos obra concluída em Jaboatão dos Guararapes. O que aparece abaixo é projeto do estúdio em outras cidades, com o lugar e o estágio indicados no cartão.',
    projects: ['clinica-esthetica', 'apartamento-rosarinho', 'casa-brut', 'apartamento-gracas'],
  },
  {
    slug: 'paulista',
    city: 'Paulista',
    region: 'Região Metropolitana do Recife',
    metaTitle: 'Arquiteto em Paulista PE',
    metaDescription:
      'Arquitetura e interiores em Paulista, do Janga a Maria Farinha e ao eixo da PE-15. Casa de veraneio, apartamento de orla e lote, com visitas agendadas.',
    h1: 'Arquitetura em Paulista, do Janga a Maria Farinha.',
    standfirst: 'Para quem constrói, reforma ou transforma um imóvel na orla ou no interior de Paulista.',
    hubNote: 'Casa de veraneio no Janga, lote em crescimento no eixo da PE-15.',
    intro: [
      'Paulista tem duas geografias. A faixa de praia — Janga, Pau Amarelo, Maria Farinha — é feita de casa de veraneio, apartamento frente-mar e terreno que alaga na maré alta. O interior, no eixo da PE-15, é outra história: lote maior, construção progressiva, casa que começa com dois quartos e cresce conforme o dinheiro aparece.',
      'Atendemos as duas, com o estúdio sediado no Recife. As etapas que pedem presença — medição, vistoria, entrega — são agendadas; o resto do projeto anda por reunião remota e documento, com o custo do deslocamento previsto no escopo.',
      'O que não muda é o ponto de partida: entender o imóvel e o uso que ele vai ter. Casa usada em dois fins de semana por mês tem exigências diferentes de casa em que se mora todos os dias, e o projeto precisa refletir isso.',
    ],
    localLens: [
      {
        place: 'Janga e Pau Amarelo',
        body: 'Orla com prédios antigos e casas apertadas entre a avenida e a praia. Ventilação cruzada e sombra resolvem mais conforto do que equipamento, e o detalhe de esquadria decide quanto tempo a fachada dura.',
      },
      {
        place: 'Maria Farinha e o mangue',
        body: 'Terreno amplo, muita água no subsolo e restinga por perto. Nível do piso, impermeabilização e drenagem entram no estudo inicial, não como correção depois da primeira chuva forte.',
      },
      {
        place: 'O eixo da PE-15',
        body: 'Paratibe, Meriú e Aurora crescem em loteamentos com construção por etapas. Projetar a estrutura para a ampliação prevista evita que a segunda fase pareça um remendo na primeira.',
      },
      {
        place: 'Casa fechada a maior parte do ano',
        body: 'Imóvel de temporada precisa ventilar sem ninguém dentro e resistir a meses fechado. Layout, aberturas e escolha de material se desenham para esse ritmo, não para o da casa permanente.',
      },
    ],
    whereWeWork:
      'O atendimento em Paulista acompanha as duas geografias da cidade. Na orla de Janga e Pau Amarelo, o caso típico é a casa de veraneio e o apartamento antigo de frente-mar; em Maria Farinha, o terreno maior, com água no subsolo e restinga por perto; no eixo da PE-15, em Paratibe, Meriú e Aurora, a casa térrea em loteamento e a construção por etapas. É essa diferença que define o partido — não um modelo trazido do Recife.',
    attendance:
      'Paulista está na Região Metropolitana. As idas ao imóvel e à obra são organizadas por etapa, em datas combinadas, com o deslocamento previsto no escopo antes da contratação.',
    faq: [
      {
        question: 'Vocês têm base em Paulista?',
        answer:
          'Não. A base é o Recife: o escritório fica no Parnamirim. Paulista entra no regime de visitas agendadas, e o projeto é conduzido no Recife entre uma visita e outra.',
      },
      {
        question: 'Há trabalho construído em Paulista?',
        answer:
          'Ainda não. O que está nesta página foi realizado em outras cidades, com a localização indicada em cada cartão. O que muda é o lugar; a forma de projetar é a mesma.',
      },
      {
        question: 'Casa usada só no verão precisa de projeto completo?',
        answer:
          'Precisa. É o imóvel que mais sofre com umidade e falta de ventilação quando fica fechado por semanas. O projeto define como a casa se comporta sozinha nos meses vazios.',
      },
      {
        question: 'Como o deslocamento entra no orçamento?',
        answer:
          'Com o número de visitas definido no escopo, antes da contratação. A distância até Paulista é curta, e a maior parte das etapas não exige presença no imóvel.',
      },
    ],
    projectsNote:
      'Ainda não há obra nossa em Paulista. Os cartões abaixo mostram casas de praia e outros projetos do estúdio, com a localização e o estágio indicados em cada um.',
    projects: ['bangalo-60-carneiros', 'bangalo-48-carneiros', 'apartamento-rosarinho', 'casa-brut'],
  },
  {
    slug: 'caruaru',
    city: 'Caruaru',
    region: 'Agreste de Pernambuco',
    metaTitle: 'Arquiteto em Caruaru',
    metaDescription:
      'Arquitetura residencial, interiores e comércio em Caruaru. Clima seco, casa que cresce por etapas e comércio de rua, com viagens agendadas a partir do Recife.',
    h1: 'Arquitetura em Caruaru, feita para o Agreste.',
    standfirst:
      'Projetos residenciais, de interiores e comerciais em Caruaru, com as etapas presenciais combinadas caso a caso.',
    hubNote: 'Clima seco, casa térrea e comércio de feira: outro jeito de construir.',
    intro: [
      'Caruaru não se projeta como o litoral. O ar é seco, o sol bate forte a maior parte do ano e a noite esfria o suficiente para mudar o comportamento da casa. Sombreamento, inércia térmica e ventilação noturna valem mais aqui do que qualquer equipamento de ar-condicionado.',
      'O estúdio fica no Recife, a pouco mais de duas horas de estrada. As visitas a Caruaru são concentradas em viagens planejadas — levantamento, vistorias em marcos da obra e entrega —, com o deslocamento no escopo desde o começo.',
      'A cidade também tem uma cultura construtiva própria: terreno generoso, casa térrea de telha cerâmica, ampliação feita aos poucos e comércio de rua girando em torno da feira. Um projeto que ignore isso vira peça de catálogo.',
    ],
    localLens: [
      {
        place: 'O sol e a amplitude térmica',
        body: 'Fachada cega onde o sol da tarde bate, proteção nos vãos e massa onde ela ajuda a segurar o fresco. A casa é desenhada para o clima antes de ser desenhada para a foto.',
      },
      {
        place: 'A noite fria do Agreste',
        body: 'A diferença entre o dia e a noite é a melhor ferramenta de conforto disponível. Pátio, abertura alta e pé-direito puxam o ar fresco para dentro e o mantêm até a tarde seguinte.',
      },
      {
        place: 'A Feira e o comércio de rua',
        body: 'A feira do Parque 18 de Maio move a cidade e define onde o comércio acontece. Loja e ponto comercial vivem do fluxo de quem passa: acesso, fachada e depósito pesam no projeto tanto quanto o salão de atendimento.',
      },
      {
        place: 'A casa que cresce por etapa',
        body: 'Muita casa começa pequena e amplia depois. Deixar estrutura, hidráulica e elétrica preparadas para a segunda fase custa pouco no início e evita obra quebrada no futuro.',
      },
      {
        place: 'Água e reservação',
        body: 'Reservatório e área técnica entram no desenho desde o estudo, com acesso para manutenção. Não são anexo decidido no fim da obra.',
      },
    ],
    whereWeWork:
      'Em Caruaru, o atendimento é voltado a projetos residenciais e a espaços comerciais de rua. Do lado residencial, predominam a casa térrea em lote próprio e a ampliação pensada desde o começo. Do lado comercial, a loja ligada à feira e às avenidas centrais. As etapas presenciais são definidas no escopo e agendadas com antecedência.',
    attendance:
      'Caruaru fica no Agreste, fora da Região Metropolitana. Levantamento, vistorias e entrega são reunidos em viagens combinadas com antecedência, e o deslocamento entra no escopo.',
    faq: [
      {
        question: 'Vocês têm base em Caruaru?',
        answer:
          'Não. A base é o Recife, no Parnamirim — a pouco mais de duas horas de estrada. Caruaru é atendida a distância, com viagens marcadas para as etapas que exigem presença.',
      },
      {
        question: 'Já construíram em Caruaru?',
        answer:
          'Ainda não. Temos projetos no Agreste e no Sertão, nas cidades indicadas em cada cartão, mas nenhum em Caruaru até agora.',
      },
      {
        question: 'Como vocês acompanham uma obra a distância?',
        answer:
          'Com vistorias nos marcos combinados no escopo — estrutura, instalações e entrega — e registro entre elas. O que precisa de decisão rápida se resolve por chamada, não por espera.',
      },
      {
        question: 'O projeto sai pronto para aprovação na prefeitura?',
        answer:
          'O executivo é entregue com as peças necessárias para a aprovação, e o acompanhamento do processo é definido no escopo. A leitura das normas do endereço acontece antes do estudo, não depois.',
      },
    ],
    projectsNote:
      'Não há obra nossa em Caruaru — e dizemos isso com clareza. Os cartões abaixo são projetos do estúdio no Agreste e no Sertão, com a cidade indicada em cada um.',
    projects: ['casa-bonito', 'casa-ipubi', 'casa-ouricuri', 'casas-geminadas-condominio'],
  },
  {
    slug: 'gravata',
    city: 'Gravatá',
    region: 'Agreste de Pernambuco',
    metaTitle: 'Arquiteto em Gravatá',
    metaDescription:
      'Arquitetura e reformas em Gravatá, com obra concluída no centro da cidade. Casa antiga, residência de serra e lote em condomínio, atendidas a partir do Recife.',
    h1: 'Arquitetura em Gravatá, com obra feita no centro.',
    standfirst: 'O estúdio tem sede no Recife e já concluiu uma reforma no centro de Gravatá.',
    hubNote: 'Reforma de casarão no centro e casa de serra — já com obra entregue.',
    intro: [
      'Em Gravatá o estúdio já entregou obra. A reforma de uma residência urbana no centro manteve o ladrilho hidráulico do piso, as soleiras de mármore e o desenho original da casa, e abriu a cozinha para a área de convivência. É o tipo de intervenção em que apagar o que existe seria mais fácil — e pior.',
      'O estúdio fica no Recife, e as visitas a Gravatá são agendadas. O deslocamento entra no escopo, combinado antes, como em qualquer outra cidade fora da capital.',
      'A cidade tem dois usos muito diferentes. Um é o centro antigo, de casarão, pé-direito alto e chuva de serra. O outro é a segunda residência, comprada por quem sai do Recife para passar o fim de semana e precisa de uma casa que funcione sozinha durante a semana.',
    ],
    localLens: [
      {
        place: 'O centro e os casarões',
        body: 'Ladrilho hidráulico, esquadria de madeira, pé-direito generoso. Levantamos o que existe antes de mexer, porque parte desse material não se repõe — e é ele que dá valor ao imóvel.',
      },
      {
        place: 'A chuva de serra',
        body: 'Na altitude, a água encontra caminho rápido. Telhado, calha, rufo e impermeabilização são detalhados junto com a esquadria, para o encontro entre parede e janela não virar infiltração na primeira temporada de chuva.',
      },
      {
        place: 'Casa de fim de semana',
        body: 'Imóvel usado em intervalos precisa de manutenção baixa, circuito simples e ventilação que funcione com a casa vazia. O layout se define por esse uso.',
      },
      {
        place: 'O Alto do Cruzeiro e a vista',
        body: 'Quem compra em Gravatá muitas vezes paga pela vista. Implantação, orientação e posição das aberturas decidem se ela aparece — e de onde.',
      },
      {
        place: 'Lote em condomínio',
        body: 'Em condomínio de serra, o terreno costuma ter aclive e regras próprias. Drenagem, acesso e recuo são resolvidos no estudo de implantação, antes de discutir fachada.',
      },
    ],
    whereWeWork:
      'A reforma concluída no centro, em 2021, é a referência para a recuperação de casarões. O atendimento também cobre a residência de fim de semana e o lote em condomínio de serra — como o projeto de casas geminadas com cobogó de tijolo aparente. São três escalas, com a mesma atenção ao que já existe no lugar.',
    attendance:
      'Gravatá fica no Agreste e as visitas entram no escopo, combinadas com antecedência — o mesmo regime da obra que já entregamos no centro.',
    faq: [
      {
        question: 'Vocês têm base em Gravatá?',
        answer:
          'Não. O escritório é no Recife, no Parnamirim, e Gravatá é atendida com visitas agendadas. O projeto avança no Recife entre uma visita e outra.',
      },
      {
        question: 'Já fizeram obra em Gravatá?',
        answer:
          'Sim. É o Casa Centro Gravatá, construído em 2021 no centro da cidade. O primeiro cartão desta página abre o projeto completo, com fotos e escopo.',
      },
      {
        question: 'Dá para reformar um casarão antigo sem descaracterizar?',
        answer:
          'Dá, e costuma ser o melhor caminho. Levantamos o que existe, separamos o que pode ser recuperado do que precisa ser refeito e desenhamos a intervenção em volta disso, não por cima.',
      },
      {
        question: 'Vocês projetam em condomínio fechado?',
        answer:
          'Sim. Há um projeto de casas geminadas em condomínio na cidade, com cobogó de tijolo aparente. O processo começa pela leitura do regulamento e pela implantação no terreno.',
      },
    ],
    projectsNote:
      'Os dois primeiros cartões são de Gravatá: um construído no centro, outro ainda em projeto. Os demais são trabalho do estúdio em outras cidades, com a localização indicada em cada um.',
    projects: ['casa-gravata', 'casas-geminadas-condominio', 'casa-bonito', 'apartamento-rosarinho'],
  },
];

/** Values for schema.org `areaServed`, city pages plus the base. */
export const AREA_SERVED = [SITE.city, ...SERVICE_AREAS.map((area) => area.city)];
