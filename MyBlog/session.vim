let SessionLoad = 1
let s:so_save = &g:so | let s:siso_save = &g:siso | setg so=0 siso=0 | setl so=-1 siso=-1
let v:this_session=expand("<sfile>:p")
silent only
silent tabonly
cd ~/Projects/Web/TimTheWebmaster/MyBlog
if expand('%') == '' && !&modified && line('$') <= 1 && getline(1) == ''
  let s:wipebuf = bufnr('%')
endif
let s:shortmess_save = &shortmess
if &shortmess =~ 'A'
  set shortmess=aoOA
else
  set shortmess=aoO
endif
badd +49 MyBlog/settings.py
badd +1 Post/urls.py
badd +8 Main/urls.py
badd +31 MyBlog/urls.py
badd +2 AnonymousComment/urls.py
badd +1 Post/views.py
badd +6 Main/templates/Main/home.html
badd +35 User/models.py
badd +7 AnonymousComment/views.py
badd +33 Post/models.py
badd +4 AnonymousComment/models.py
badd +65 Main/templates/Main/base.html
badd +122 Post/templates/Post/base_post.html
badd +20 Comment/models.py
badd +28 User/admin.py
badd +4 Main/views.py
badd +9 User/views.py
badd +66 Comment/views.py
badd +37 Post/static/Post/js/comments.js
badd +198 Main/static/Main/css/blocks.css
badd +40 User/static/User/css/comment.css
badd +9 Comment/urls.py
badd +1 User/static/User/js/add_comment.js
badd +1 Post/templates/Post/table_of_content.html
badd +1 Main/static/Main/css/buttons.css
badd +137 Comment/static/Comment/js/comments.js
badd +31 Main/templates/Main/contacts.html
badd +1 User/static/User/css/forms.css
badd +1 Main/static/Main/js/button.js
argglobal
%argdel
edit Comment/static/Comment/js/comments.js
let s:save_splitbelow = &splitbelow
let s:save_splitright = &splitright
set splitbelow splitright
wincmd _ | wincmd |
vsplit
1wincmd h
wincmd _ | wincmd |
split
1wincmd k
wincmd w
wincmd w
wincmd _ | wincmd |
split
1wincmd k
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
exe '1resize ' . ((&lines * 24 + 26) / 53)
exe 'vert 1resize ' . ((&columns * 94 + 94) / 189)
exe '2resize ' . ((&lines * 25 + 26) / 53)
exe 'vert 2resize ' . ((&columns * 94 + 94) / 189)
exe '3resize ' . ((&lines * 26 + 26) / 53)
exe 'vert 3resize ' . ((&columns * 94 + 94) / 189)
exe '4resize ' . ((&lines * 23 + 26) / 53)
exe 'vert 4resize ' . ((&columns * 94 + 94) / 189)
argglobal
balt Post/templates/Post/base_post.html
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
let s:l = 125 - ((9 * winheight(0) + 12) / 24)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 125
normal! 043|
wincmd w
argglobal
if bufexists(fnamemodify("Post/templates/Post/base_post.html", ":p")) | buffer Post/templates/Post/base_post.html | else | edit Post/templates/Post/base_post.html | endif
if &buftype ==# 'terminal'
  silent file Post/templates/Post/base_post.html
endif
balt Comment/static/Comment/js/comments.js
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
let s:l = 110 - ((7 * winheight(0) + 12) / 25)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 110
normal! 054|
wincmd w
argglobal
if bufexists(fnamemodify("Comment/urls.py", ":p")) | buffer Comment/urls.py | else | edit Comment/urls.py | endif
if &buftype ==# 'terminal'
  silent file Comment/urls.py
endif
balt Comment/static/Comment/js/comments.js
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
let s:l = 9 - ((7 * winheight(0) + 13) / 26)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 9
normal! 026|
lcd ~/Projects/Web/TimTheWebmaster/MyBlog
wincmd w
argglobal
if bufexists(fnamemodify("~/Projects/Web/TimTheWebmaster/MyBlog/Comment/views.py", ":p")) | buffer ~/Projects/Web/TimTheWebmaster/MyBlog/Comment/views.py | else | edit ~/Projects/Web/TimTheWebmaster/MyBlog/Comment/views.py | endif
if &buftype ==# 'terminal'
  silent file ~/Projects/Web/TimTheWebmaster/MyBlog/Comment/views.py
endif
balt ~/Projects/Web/TimTheWebmaster/MyBlog/Post/views.py
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
let s:l = 68 - ((14 * winheight(0) + 11) / 23)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 68
normal! 0
lcd ~/Projects/Web/TimTheWebmaster/MyBlog
wincmd w
3wincmd w
exe '1resize ' . ((&lines * 24 + 26) / 53)
exe 'vert 1resize ' . ((&columns * 94 + 94) / 189)
exe '2resize ' . ((&lines * 25 + 26) / 53)
exe 'vert 2resize ' . ((&columns * 94 + 94) / 189)
exe '3resize ' . ((&lines * 26 + 26) / 53)
exe 'vert 3resize ' . ((&columns * 94 + 94) / 189)
exe '4resize ' . ((&lines * 23 + 26) / 53)
exe 'vert 4resize ' . ((&columns * 94 + 94) / 189)
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
