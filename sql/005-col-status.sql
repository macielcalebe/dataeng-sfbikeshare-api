ALTER TABLE public.status
  ADD COLUMN category1 INTEGER NULL,
  ADD COLUMN category2 INTEGER NULL;

-- Descomente caso queira explorar estas colunas
-- UPDATE public.status
-- SET category1 = floor(random() * 3)::INTEGER,
--     category2 = floor(random() * 10000)::INTEGER;
