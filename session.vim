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
badd +121 MyBlog/Comment/views.py
badd +47 MyBlog/Comment/static/Comment/js/comments.js
badd +86 MyBlog/Post/templates/Post/base_post.html
badd +2 MyBlog/Main/migrations/0003_downloadable_text_en_downloadable_text_ru_and_more.py
badd +28 TODO.md
badd +1 MyBlog/Post/views.py
badd +20 MyBlog/Comment/models.py
badd +15 MyBlog/Comment/urls.py
badd +29 MyBlog/User/static/User/js/add_comment.js
badd +9 MyBlog/Comment/templates/Comment/comment.html
badd +1 MyBlog/Comment/templates/Comment/comments.html
badd +1 MyBlog/User/admin.py
badd +13 MyBlog/Comment/admin.py
badd +19 MyBlog/Post/urls.py
badd +62 MyBlog/Main/templates/Main/base.html
argglobal
%argdel
edit MyBlog/Post/templates/Post/base_post.html
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
balt MyBlog/Comment/templates/Comment/comment.html
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
let s:l = 129 - ((16 * winheight(0) + 24) / 49)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 129
normal! 0119|
lcd ~/Projects/Web/TimTheWebmaster
wincmd w
argglobal
if bufexists(fnamemodify("~/Projects/Web/TimTheWebmaster/MyBlog/Comment/static/Comment/js/comments.js", ":p")) | buffer ~/Projects/Web/TimTheWebmaster/MyBlog/Comment/static/Comment/js/comments.js | else | edit ~/Projects/Web/TimTheWebmaster/MyBlog/Comment/static/Comment/js/comments.js | endif
if &buftype ==# 'terminal'
  silent file ~/Projects/Web/TimTheWebmaster/MyBlog/Comment/static/Comment/js/comments.js
endif
balt ~/Projects/Web/TimTheWebmaster/MyBlog/Comment/views.py
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
let s:l = 214 - ((44 * winheight(0) + 24) / 49)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 214
normal! 010|
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
