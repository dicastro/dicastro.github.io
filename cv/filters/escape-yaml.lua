local pandoc = require("pandoc")

local domain = "https://diegocastroviadero.com"

-- Reformat dates and generate fields _my and _y
local function processDates(t)
  for k,v in pairs(t) do
    if type(v) == "table" and #v == 1 and v[1].t == "Str" then
      local str = v[1].text
      local y,m,d = str:match("(%d+)-(%d+)-(%d+)")
      if y and m and d then
        -- replaces original date
        t[k][1] = pandoc.Str(string.format("%02d/%02d/%04d", d,m,y))
        -- additional keys
        t[k .. "_my"] = { pandoc.Str(string.format("%02d/%04d", m,y)) }
        t[k .. "_y"]  = { pandoc.Str(string.format("%04d", y)) }
      end
    elseif type(v) == "table" then
      processDates(v) -- recursive
    end
  end
end

-- Converts relative URLs to absolute URLs in simple Str
local function processStrUrls(t)
  for k,v in pairs(t) do
    if type(v) == "table" then
      for i,e in ipairs(v) do
        if e.t == "Str" and e.text:match("^/") then
          v[i] = pandoc.Str(domain .. e.text)
        elseif type(e) == "table" then
          processStrUrls({ [1] = e })
        end
      end
      processStrUrls(v)
    end
  end
end

-- Converts relative URLs inside Link
local function processInlines(inlines)
  local out = {}

  local i = 1

  while i <= #inlines do
    local inline = inlines[i]

    if inline.t == "Link" then
      if inline.target:match("^/") then
        inline.target = domain .. inline.target
      end

      inline.content = processInlines(inline.content)

      table.insert(out, inline)
    elseif inline.t == "RawInline" and inline.format == "html" and inline.text:match("^<icon.*") then
      local html = inline.text

      local fa = html:match('fa%s*=%s*"([^"]+)"') or html:match('fa%-name%s*=%s*"([^"]+)"')

      fa = fa or "Question"

      local texts = {}
      local j = i + 1
      while j <= #inlines do
        local nextInline = inlines[j]
        if nextInline.t == "Str" and (nextInline.text == "{{" or nextInline.text == "}}") then
          j = j + 1
        elseif nextInline.t == "Str" or nextInline.t == "Space" then
          table.insert(texts, pandoc.utils.stringify(nextInline))
          j = j + 1
        else
          break
        end
      end

      local secondArg = table.concat(texts, "")

      table.insert(out, pandoc.RawInline("latex", "\\faicon{" .. fa .. "}{" .. secondArg .. "}"))

      i = j - 1
    elseif inline.t == "Str" and (inline.text == "{{" or inline.text == "}}") then
      -- do nothing
    elseif inline.content then
      inline.content = processInlines(inline.content)
      table.insert(out, inline)
    else
      table.insert(out, inline)
    end

    i = i + 1
  end

  return out
end

-- Iterates blocks like BulletList, Plain, Para
local function processBlocks(blocks)
  for _, blk in ipairs(blocks) do
    if blk.t == "BulletList" or blk.t == "OrderedList" then
      for _, sublist in ipairs(blk.content) do
        processBlocks(sublist)
      end
    elseif blk.content then
      if type(blk.content) == "table" then
        processBlocks(blk.content)
      end
    end
    if blk.t == "Plain" or blk.t == "Para" then
      blk.content = processInlines(blk.content)
    end
  end
end

-- Remove completely empty lines from LaTeX string
local function removeEmptyLines(latex)
  local lines = {}
  for line in latex:gmatch("[^\r\n]+") do
    if not line:match("^%s*$") then
      table.insert(lines, line)
    end
  end
  return table.concat(lines, "\n")
end

local function removeListBreaks(latex)
  return latex
    :gsub("\\begin{itemize}(.-)\\end{itemize}", function(block)
      block = block:gsub("\\\\%s*\n", "\n")
      return "\\begin{itemize}" .. block .. "\\end{itemize}"
    end)
    :gsub("\\begin{enumerate}(.-)\\end{enumerate}", function(block)
      block = block:gsub("\\\\%s*\n", "\n")
      return "\\begin{enumerate}" .. block .. "\\end{enumerate}"
    end)
end

-- Join list items split across two lines
local function fixSplitItems(latex)
  -- Replace: \item\nSomething  →  \item Something
  return latex:gsub("\\item%s*\n%s*", "\\item ")
end


-- Convert most newlines to LaTeX linebreaks (\\) except for special cases
local function addLineBreaksExcept(latex)
  local output = {}

  for line in latex:gmatch("([^\n]*)\n?") do
    if line == "" then goto continue end

    local trimmed = line:gsub("%s+$", "")

    -- EXCEPTIONS: do NOT add '\\'
    if trimmed:match("\\begin{itemize}$")
      or trimmed:match("\\end{itemize}$")
      or trimmed:match("\\tightlist$")
      or trimmed:match("\\begin{enumerate}$")
      or trimmed:match("\\end{enumerate}$")
      or trimmed:match("\\def\\labelenumi.*")
      or trimmed:match("^\\item%s*")
      or trimmed:match("^\\header*") then
      table.insert(output, trimmed)
    else
      -- Normal text → add '\\'
      --table.insert(output, trimmed .. "\\\\")
      table.insert(output, trimmed)
    end

    ::continue::
  end

  -- Remove a trailing '\\' at the very end of the output
  local result = table.concat(output, "\n")
  result = result:gsub("\\\\%s*$", "")

  return result
end


-- Convert Pandoc blocks to LaTeX safely for cventry
local function blocksToSafeLatex(blocks)
  local doc = pandoc.Pandoc(blocks)

  local latex = pandoc.pipe("pandoc", {
    "--from=markdown",
    "--to=latex",
    "--wrap=none"
  }, pandoc.write(doc, "markdown"))

  latex = removeEmptyLines(latex)
  latex = removeListBreaks(latex)
  latex = fixSplitItems(latex)
  latex = addLineBreaksExcept(latex)

  return latex
end

-- Sanitize a summary field
local function sanitizeSummaryField(field)
  if not field then return nil end
  -- Convert to Pandoc blocks if it's a MetaString or MetaBlocks
  local blocks = {}
  if field.t == "MetaString" or field.t == "MetaInlines" then
    blocks = pandoc.read(pandoc.utils.stringify(field), "markdown").blocks
  elseif field.t == "MetaBlocks" or type(field) == "table" then
    blocks = field
  else
    return nil
  end

  local latex = blocksToSafeLatex(blocks)
  -- Wrap in minipage for cventry safety
  --local wrapped = "{\\begin{minipage}{\\linewidth}\n" .. latex .. "\n\\end{minipage}}"
  --return pandoc.RawBlock("latex", wrapped)

  return pandoc.RawBlock("latex", latex)
end

-- Aplica la sanitización a listas de items en meta (work, education, ...)
local function sanitizeListOfItems(list)
  if type(list) ~= "table" then return end

  for _, item in ipairs(list) do
    if type(item) == "table" and item.summary then
      local sanitized = sanitizeSummaryField(item.summary)
  
      if sanitized then
        item.summary = sanitized
      else
        item.summary = nil
      end
    end
  end
end

local function processMeta(meta)
  processDates(meta)
  processStrUrls(meta)

  for _, v in pairs(meta) do
    if type(v) == "table" then
      if v[1] and v[1].t then
        processBlocks(v)
      else
        processMeta(v)
      end
    end
  end

  sanitizeListOfItems(meta.work)
  sanitizeListOfItems(meta.education)
end

function Header(el)
  if el.level == 4 then
    local latex = "\\headerliiii{" .. pandoc.utils.stringify(el.content) .. "}"

    return pandoc.RawInline("latex", latex)
  end
end

function Meta(meta)
  processMeta(meta)

  return meta
end