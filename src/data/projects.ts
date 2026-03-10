export interface Project {
  order: number;
  title: string;
  description: string;
  url: string;
  tags: string[];
  briefNumber?: number;
  image?: string;
}

export const projects: Project[] = [
  {
    order: 1,
    title: "Tic-Tac-Toe vs AI",
    description: "Premier projet pour se familiariser avec Python, remis au goût du jour : le morpion en CLI est devenu une app web full-stack avec une IA Minimax imbattable.",
    url: "https://tictactoe.dvdjnbr.fr/",
    tags: ["Python", "Flask", "JavaScript"],
    briefNumber: 1,
    image: "https://picsum.photos/seed/tictactoe/600/400"
  },
  {
    order: 2,
    title: "Qualité de l'eau potable — France 2024",
    description: "L'eau potable française comme terrain pour apprendre Azure/Databricks de bout en bout — ingestion Hub'Eau, pipeline Medallion Bronze→Gold, star schema analytique et API REST qui tourne sans compute actif.",
    url: "https://qlt-eau-fr-24.dvdjnbr.fr/",
    tags: ["Python", "FastAPI", "Databricks", "Azure", "Terraform"],
    image: "https://picsum.photos/seed/water/600/400"
  },
  {
    order: 3,
    title: "Portfolio Astro",
    description: "Le portfolio sur lequel vous naviguez actuellement, construit avec Astro et un peu de magie CSS 3D.",
    url: "https://dvdjnbr.fr",
    tags: ["Astro", "TypeScript", "CSS"],
    image: "https://picsum.photos/seed/portfolio/600/400"
  }
];
