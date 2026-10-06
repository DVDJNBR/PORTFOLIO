export const TAG_BADGES: Record<string, string> = {
  Python: 'https://img.shields.io/badge/python-%233670A0.svg?style=for-the-badge&logo=python&logoColor=ffdd54',
  Databricks: 'https://img.shields.io/badge/Databricks-%23FF3621.svg?style=for-the-badge&logo=databricks&logoColor=white',
  Azure: 'https://img.shields.io/badge/azure-%230078D4.svg?style=for-the-badge&logo=microsoftazure&logoColor=white',
  'Azure Functions': 'https://img.shields.io/badge/Azure%20Functions-%230062AD.svg?style=for-the-badge&logo=azurefunctions&logoColor=white',
  'Delta Lake': 'https://img.shields.io/badge/Delta%20Lake-00ADD8.svg?style=for-the-badge',
  Terraform: 'https://img.shields.io/badge/terraform-%235835CC.svg?style=for-the-badge&logo=terraform&logoColor=white',
  Snowflake: 'https://img.shields.io/badge/snowflake-%2329B5E8.svg?style=for-the-badge&logo=snowflake&logoColor=white',
  dbt: 'https://img.shields.io/badge/dbt-%23FF694B.svg?style=for-the-badge&logo=dbt&logoColor=white',
  Streamlit: 'https://img.shields.io/badge/Streamlit-%23FE4B4B.svg?style=for-the-badge&logo=streamlit&logoColor=white',
  Docker: 'https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white',
  FastAPI: 'https://img.shields.io/badge/fastapi-%23009688.svg?style=for-the-badge&logo=fastapi&logoColor=white',
  React: 'https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB',
  Supabase: 'https://img.shields.io/badge/Supabase-%233ECF8E.svg?style=for-the-badge&logo=supabase&logoColor=white',
};

export const tagBadge = (tag: string): string =>
  TAG_BADGES[tag] ?? `https://img.shields.io/badge/${encodeURIComponent(tag)}-8f8c86.svg?style=for-the-badge`;
