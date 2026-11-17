-- Parte 4 - Exercícios com SQL (banco db.sqlite3 gerado pelo Django)
-- Tabelas: blog_post, blog_comment, blog_category, blog_category_posts, auth_user
-- Os filtros usam o título do post / nome da categoria, para não depender dos ids.

-- 1. Todos os posts, ordenados pela data, sendo o mais recente primeiro
SELECT *
FROM blog_post
ORDER BY date DESC;

-- 2. Para um post com comentários, todos os seus comentários
SELECT *
FROM blog_comment
WHERE post_id = (SELECT id FROM blog_post WHERE title = 'Primeiros passos com Django');

-- 3. Para um post com comentários, todos os seus comentários (todas as colunas
--    exceto post_id), o título do post e sua data de publicação como post_date
SELECT c.id,
       c.text,
       c.date,
       c.author_id,
       p.title,
       p.date AS post_date
FROM blog_comment AS c
JOIN blog_post AS p ON p.id = c.post_id
WHERE p.title = 'Primeiros passos com Django';

-- 4. Para uma categoria, todos os posts pertencentes a ela, com as colunas
--    da tabela de categoria e da tabela de posts
SELECT cat.id AS category_id,
       cat.name,
       cat.description,
       p.id AS post_id,
       p.title,
       p.content,
       p.date
FROM blog_category AS cat
JOIN blog_category_posts AS cp ON cp.category_id = cat.id
JOIN blog_post AS p ON p.id = cp.post_id
WHERE cat.name = 'Automação';

-- 5. Todas as categorias que possuem dois ou mais posts
SELECT cat.id,
       cat.name,
       cat.description,
       COUNT(cp.post_id) AS num_posts
FROM blog_category AS cat
JOIN blog_category_posts AS cp ON cp.category_id = cat.id
GROUP BY cat.id, cat.name, cat.description
HAVING COUNT(cp.post_id) >= 2;
