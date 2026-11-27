function Table(t)
  local n = #t.colspecs
  local first = pandoc.utils.stringify(t.head.rows[1].cells[1].contents)
  local widths
  if n >= 5 then
    local first_width = n >= 7 and 0.34 or 0.39
    widths = {first_width}
    for i = 2,n do
      widths[i] = (1 - first_width) / (n - 1)
      t.colspecs[i][1] = 'AlignCenter'
    end
    local labels = {
      ['Entrada']='Fonte', ['Exemplos']='Exemp.', ['Léxica']='Léx.',
      ['Sintática']='Sint.', ['Derivação']='Deriv.', ['Semânt.']='Sem.',
      ['Geração']='Geraç.', ['Aprendizagem']='Aprendiz.'
    }
    for i=2,n do
      local cell = t.head.rows[1].cells[i]
      local label = labels[pandoc.utils.stringify(cell.contents)]
      if label then cell.contents = {pandoc.Plain({pandoc.Str(label)})} end
    end
  elseif n == 4 then
    widths = {0.31,0.23,0.23,0.23}
  elseif n == 3 then
    widths = {0.30,0.40,0.30}
    if first == 'Código' then widths = {0.09,0.68,0.23}
    elseif first == 'Caso' then widths = {0.09,0.48,0.43}
    elseif first == 'Verificação' then widths = {0.39,0.30,0.31} end
  elseif n == 2 then
    widths = {0.28,0.72}
  end
  if widths then
    for i=1,n do t.colspecs[i][2] = widths[i] end
  end
  if FORMAT == 'latex' then
    return {pandoc.RawBlock('latex','\\begingroup\\small'), t, pandoc.RawBlock('latex','\\endgroup')}
  end
  return t
end

function Header(h)
  if FORMAT == 'latex' then
    local s = pandoc.utils.stringify(h.content)
    if s:match('^2%.[123]%.') then
      return {pandoc.RawBlock('latex','\\Needspace{23\\baselineskip}'), h}
    end
  end
  return h
end
