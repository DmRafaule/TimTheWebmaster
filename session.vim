let SessionLoad = 1
let s:so_save = &g:so | let s:siso_save = &g:siso | setg so=0 siso=0 | setl so=-1 siso=-1
let v:this_session=expand("<sfile>:p")
silent only
silent tabonly
cd ~/Projects/Web/TimTheWebmaster
if expand('%') == '' && !&modified && line('$') <= 1 && getline(1) == ''
  let s:wipebuf = bufnr('%')
endif
let s:shortmess_save = &shortmess
if &shortmess =~ 'A'
  set shortmess=aoOA
else
  set shortmess=aoO
endif
badd +111 MyBlog/Post/models.py
badd +1485 .venv/lib/python3.11/site-packages/django/db/models/fields/__init__.py
badd +44 MyBlog/Post/admin.py
badd +28 MyBlog/Main/translation.py
badd +29 MyBlog/Post/templates/Post/list--post_preview-tools.html
badd +116 MyBlog/Post/views.py
badd +11 MyBlog/Comment/models.py
badd +45 MyBlog/User/models.py
badd +20 ~/.local/share/nvim/mason/packages/python-lsp-server/venv/lib/python3.11/site-packages/jedi/third_party/django-stubs/django-stubs/db/models/base.pyi
badd +1 MyBlog/Main/urls.py
badd +69 MyBlog/Post/urls.py
badd +31 MyBlog/Main/static/Main/js/home.js
badd +48 MyBlog/Main/views.py
badd +1 MyBlog/Main/utils.py
badd +104 MyBlog/ImageThief/Utils/utils.py
badd +1 MyBlog/User/views.py
badd +1 MyBlog/Comment/views.py
badd +1 MyBlog/Post/templates/Post/base_post_list.html
badd +87 MyBlog/Post/static/Post/js/sorting.js
badd +1 MyBlog/Post/static/Post/js/infinity_scroll.js
badd +6 MyBlog/Post/templates/Post/basic--post_preview-home.html
badd +9 MyBlog/Post/templates/Post/basic--post_preview-home-articles.html
badd +9 MyBlog/Post/templates/Post/basic--post_preview-home-cases.html
badd +9 MyBlog/Post/templates/Post/basic--post_preview-home-news.html
badd +67 MyBlog/Main/templates/Main/home.html
badd +25 MyBlog/Post/static/Post/js/more.js
badd +11 MyBlog/Post/templates/Post/basic--post_preview-articles.html
badd +5 MyBlog/Post/static/Post/css/posts_preview.css
badd +19 MyBlog/Main/static/images.css
badd +10 MyBlog/Post/templates/Post/simple--post_preview-articles.html
badd +9 MyBlog/Post/templates/Post/minimal--post_preview-articles.html
badd +1 MyBlog/Main/static/buttons.css
badd +17 MyBlog/Post/templates/Post/raw--post_preview-articles.html
badd +9 MyBlog/Post/templates/Post/simple--post_preview-news.html
badd +11 MyBlog/Post/templates/Post/basic--post_preview-news.html
badd +9 MyBlog/Post/templates/Post/minimal--post_preview-news.html
badd +1 MyBlog/Post/templates/Post/raw--post_preview-news.html
badd +9 MyBlog/Post/templates/Post/simple--post_preview-cases.html
badd +11 MyBlog/Post/templates/Post/basic--post_preview-cases.html
badd +9 MyBlog/Post/templates/Post/minimal--post_preview-cases.html
badd +1 MyBlog/Post/static/Post/css/post.css
badd +4 MyBlog/Post/templates/Post/grid--post_preview-tools.html
badd +1 MyBlog/Post/templates/Post/basic--post_preview-qa.html
badd +1 MyBlog/Post/templates/Post/extended--post_preview-qa.html
badd +141 MyBlog/Main/templates/Main/base.html
badd +1 MyBlog/Main/static/toggle_button.js
badd +26 MyBlog/Post/templates/Post/termin_list.html
badd +1 MyBlog/Post/static/Post/js/toggle_termin.js
badd +23 MyBlog/Post/templates/Post/product_list.html
badd +15 MyBlog/Main/static/config.css
badd +81 MyBlog/Main/static/blocks.css
badd +10 MyBlog/Post/templates/Post/basic--post_preview-td.html
badd +1 MyBlog/Post/templates/Post/extended--post_preview-td.html
badd +14 MyBlog/Post/templates/Post/list--post_preview-services.html
badd +15 MyBlog/Post/templates/Post/grid--post_preview-services.html
badd +43 MyBlog/Post/templates/Post/qa.html
badd +1 MyBlog/Post/templates/Post/post.html
badd +13 MyBlog/Post/templates/Post/base_post.html
badd +32 MyBlog/Post/templates/Post/article.html
badd +54 MyBlog/Post/templates/Post/news.html
badd +96 MyBlog/Post/templates/Post/base_article.html
badd +24 MyBlog/Post/templates/Post/case.html
badd +7 MyBlog/Post/templates/Post/td.html
badd +7 MyBlog/Post/templates/Post/service.html
badd +75 MyBlog/Comment/static/Comment/js/comments.js
badd +1 MyBlog/Comment/static/Comment/js/feedback.js
badd +5 ~/Documents/Posts/articles/kak-realizovat-registraciyu-i-logirovanie-polzovatelej/HowToMakeAuthenticationSystem.html
badd +1 MyBlog/Post/static/Post/css/news.css
badd +8 MyBlog/Main/static/text.css
badd +96 MyBlog/Main/static/layout.css
badd +12 MyBlog/Post/templatetags/markdown.py
badd +12 MyBlog/Main/static/lists.css
badd +2 MyBlog/Main/static/Main/css/home.css
badd +14 MyBlog/Post/static/Post/css/case.css
badd +23 MyBlog/Post/static/Post/js/tabs.js
badd +39 MyBlog/Post/static/Post/css/tabs.css
badd +42 MyBlog/Main/static/media_loader.js
argglobal
%argdel
edit MyBlog/Post/static/Post/css/tabs.css
let s:save_splitbelow = &splitbelow
let s:save_splitright = &splitright
set splitbelow splitright
wincmd _ | wincmd |
vsplit
1wincmd h
wincmd w
let &splitbelow = s:save_splitbelow
let &splitright = s:save_splitright
wincmd t
let s:save_winminheight = &winminheight
let s:save_winminwidth = &winminwidth
set winminheight=0
set winheight=1
set winminwidth=0
set winwidth=1
exe 'vert 1resize ' . ((&columns * 92 + 94) / 189)
exe 'vert 2resize ' . ((&columns * 96 + 94) / 189)
argglobal
balt MyBlog/Post/static/Post/css/case.css
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let &fdl = &fdl
let s:l = 4 - ((3 * winheight(0) + 25) / 50)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 4
normal! 0
lcd ~/Projects/Web/TimTheWebmaster
wincmd w
argglobal
if bufexists(fnamemodify("~/Projects/Web/TimTheWebmaster/MyBlog/Post/templates/Post/case.html", ":p")) | buffer ~/Projects/Web/TimTheWebmaster/MyBlog/Post/templates/Post/case.html | else | edit ~/Projects/Web/TimTheWebmaster/MyBlog/Post/templates/Post/case.html | endif
if &buftype ==# 'terminal'
  silent file ~/Projects/Web/TimTheWebmaster/MyBlog/Post/templates/Post/case.html
endif
balt ~/Projects/Web/TimTheWebmaster/MyBlog/Post/templates/Post/news.html
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let &fdl = &fdl
let s:l = 70 - ((37 * winheight(0) + 25) / 50)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 70
normal! 015|
lcd ~/Projects/Web/TimTheWebmaster
wincmd w
exe 'vert 1resize ' . ((&columns * 92 + 94) / 189)
exe 'vert 2resize ' . ((&columns * 96 + 94) / 189)
tabnext 1
if exists('s:wipebuf') && len(win_findbuf(s:wipebuf)) == 0 && getbufvar(s:wipebuf, '&buftype') isnot# 'terminal'
  silent exe 'bwipe ' . s:wipebuf
endif
unlet! s:wipebuf
set winheight=1 winwidth=20
let &shortmess = s:shortmess_save
let &winminheight = s:save_winminheight
let &winminwidth = s:save_winminwidth
let s:sx = expand("<sfile>:p:r")."x.vim"
if filereadable(s:sx)
  exe "source " . fnameescape(s:sx)
endif
let &g:so = s:so_save | let &g:siso = s:siso_save
set hlsearch
doautoall SessionLoadPost
unlet SessionLoad
" vim: set ft=vim :
