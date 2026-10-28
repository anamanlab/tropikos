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

export const NAV_LINKS = [
  { label: 'Projetos', href: '/projetos', index: '01' },
  { label: 'Estúdio', href: '/estudio', index: '02' },
  { label: 'Serviços', href: '/servicos', index: '03' },
  { label: 'Contato', href: '/contato', index: '04' },
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
