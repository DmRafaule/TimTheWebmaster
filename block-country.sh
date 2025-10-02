#!/usr/bin/bash

COUNTRY_CODE="$2"
INPUT_FILE="$COUNTRY_CODE-ip-groups.txt"
OUTPUT_FILE=".htaccess"
TO_DOWNLOAD_URL="https://www.ipdeny.com/ipblocks/data/countries/$COUNTRY_CODE.zone"
BLOCK_START="##$COUNTRY_CODE START"
BLOCK_END="##$COUNTRY_CODE END"
PREFIX="Deny from"
ALLOWED_ACTIONS=("--add" "--remove" "--update")
ALLOWED_CODES=(aa 	ab 	ac 	ad 	ae 	af 	ag 	ah 	ai 	aj 	ak 	al 	am 	an 	ao 	ap 	aq 	ar 	as 	at 	au 	av 	aw 	ax 	ay 	az
ba 	bb 	bc 	bd 	be 	bf 	bg 	bh 	bi 	bj 	bk 	bl 	bm 	bn 	bo 	bp 	bq 	br 	bs 	bt 	bu 	bv 	bw 	bx 	by 	bz
ca 	cb 	cc 	cd 	ce 	cf 	cg 	ch 	ci 	cj 	ck 	cl 	cm 	cn 	co 	cp 	cq 	cr 	cs 	ct 	cu 	cv 	cw 	cx 	cy 	cz
da 	db 	dc 	dd 	de 	df 	dg 	dh 	di 	dj 	dk 	dl 	dm 	dn 	"do" dp	dq 	dr 	ds 	dt 	du 	dv 	dw 	dx 	dy 	dz
ea 	eb 	ec 	ed 	ee 	ef 	eg 	eh 	ei 	ej 	ek 	el 	em 	en 	eo 	ep 	eq 	er 	es 	et 	eu 	ev 	ew 	ex 	ey 	ez
fa 	fb 	fc 	fd 	fe 	ff 	fg 	fh 	"fi" fj	fk 	fl 	fm 	fn 	fo 	fp 	fq 	fr 	fs 	ft 	fu 	fv 	fw 	fx 	fy 	fz
ga 	gb 	gc 	gd 	ge 	gf 	gg 	gh 	gi 	gj 	gk 	gl 	gm 	gn 	go 	gp 	gq 	gr 	gs 	gt 	gu 	gv 	gw 	gx 	gy 	gz
ha 	hb 	hc 	hd 	he 	hf 	hg 	hh 	hi 	hj 	hk 	hl 	hm 	hn 	ho 	hp 	hq 	hr 	hs 	ht 	hu 	hv 	hw 	hx 	hy 	hz
ia 	ib 	ic 	id 	ie 	"if" ig	ih 	ii 	ij 	ik 	il 	im 	in 	io 	ip 	iq 	ir 	is 	it 	iu 	iv 	iw 	ix 	iy 	iz
ja 	jb 	jc 	jd 	je 	jf 	jg 	jh 	ji 	jj 	jk 	jl 	jm 	jn 	jo 	jp 	jq 	jr 	js 	jt 	ju 	jv 	jw 	jx 	jy 	jz
ka 	kb 	kc 	kd 	ke 	kf 	kg 	kh 	ki 	kj 	kk 	kl 	km 	kn 	ko 	kp 	kq 	kr 	ks 	kt 	ku 	kv 	kw 	kx 	ky 	kz
la 	lb 	lc 	ld 	le 	lf 	lg 	lh 	li 	lj 	lk 	ll 	lm 	ln 	lo 	lp 	lq 	lr 	ls 	lt 	lu 	lv 	lw 	lx 	ly 	lz
ma 	mb 	mc 	md 	me 	mf 	mg 	mh 	mi 	mj 	mk 	ml 	mm 	mn 	mo 	mp 	mq 	mr 	ms 	mt 	mu 	mv 	mw 	mx 	my 	mz
na 	nb 	nc 	nd 	ne 	nf 	ng 	nh 	ni 	nj 	nk 	nl 	nm 	nn 	no 	np 	nq 	nr 	ns 	nt 	nu 	nv 	nw 	nx 	ny 	nz
oa 	ob 	oc 	od 	oe 	of 	og 	oh 	oi 	oj 	ok 	ol 	om 	on 	oo 	op 	oq 	or 	os 	ot 	ou 	ov 	ow 	ox 	oy 	oz
pa 	pb 	pc 	pd 	pe 	pf 	pg 	ph 	pi 	pj 	pk 	pl 	pm 	pn 	po 	pp 	pq 	pr 	ps 	pt 	pu 	pv 	pw 	px 	py 	pz
qa 	qb 	qc 	qd 	qe 	qf 	qg 	qh 	qi 	qj 	qk 	ql 	qm 	qn 	qo 	qp 	qq 	qr 	qs 	qt 	qu 	qv 	qw 	qx 	qy 	qz
ra 	rb 	rc 	rd 	re 	rf 	rg 	rh 	ri 	rj 	rk 	rl 	rm 	rn 	ro 	rp 	rq 	rr 	rs 	rt 	ru 	rv 	rw 	rx 	ry 	rz
sa 	sb 	sc 	sd 	se 	sf 	sg 	sh 	si 	sj 	sk 	sl 	sm 	sn 	so 	sp 	sq 	sr 	ss 	st 	su 	sv 	sw 	sx 	sy 	sz
ta 	tb 	tc 	td 	te 	tf 	tg 	th 	ti 	tj 	tk 	tl 	tm 	tn 	to 	tp 	tq 	tr 	ts 	tt 	tu 	tv 	tw 	tx 	ty 	tz
ua 	ub 	uc 	ud 	ue 	uf 	ug 	uh 	ui 	uj 	uk 	ul 	um 	un 	uo 	up 	uq 	ur 	us 	ut 	uu 	uv 	uw 	ux 	uy 	uz
va 	vb 	vc 	vd 	ve 	vf 	vg 	vh 	vi 	vj 	vk 	vl 	vm 	vn 	vo 	vp 	vq 	vr 	vs 	vt 	vu 	vv 	vw 	vx 	vy 	vz
wa 	wb 	wc 	wd 	we 	wf 	wg 	wh 	wi 	wj 	wk 	wl 	wm 	wn 	wo 	wp 	wq 	wr 	ws 	wt 	wu 	wv 	ww 	wx 	wy 	wz
xa 	xb 	xc 	xd 	xe 	xf 	xg 	xh 	xi 	xj 	xk 	xl 	xm 	xn 	xo 	xp 	xq 	xr 	xs 	xt 	xu 	xv 	xw 	xx 	xy 	xz
ya 	yb 	yc 	yd 	ye 	yf 	yg 	yh 	yi 	yj 	yk 	yl 	ym 	yn 	yo 	yp 	yq 	yr 	ys 	yt 	yu 	yv 	yw 	yx 	yy 	yz
za 	zb 	zc 	zd 	ze 	zf 	zg 	zh 	zi 	zj 	zk 	zl 	zm 	zn 	zo 	zp 	zq 	zr 	zs 	zt 	zu 	zv 	zw 	zx 	zy 	zz)


# Send message depends on status codes
status() {
    if [ $? -eq 0 ]; then
        echo "  OK: $1"
    else
        echo "  ERR: $2"
        exit
    fi
}

# Check if first value in array
has_arg() {
    local term="$1"
    local array_name="$2[@]"
    local array=("${!array_name}")
    shift
    for array_element in ${array[@]} ; do
        if [[ $array_element == "$term" ]]; then
            return 0
        fi
    done
    return 1
}

# Download the file contains the IP's
download_the_ips() {
    STATUS_CODE="$(curl -s -o /dev/null -w "%{http_code}" $TO_DOWNLOAD_URL)"
    if [ "$STATUS_CODE" != "200" ]; then
        echo "ERROR: Couldn't find the source: $TO_DOWNLOAD_URL"
        exit
    fi
    curl -L $TO_DOWNLOAD_URL > $INPUT_FILE
    echo "SUCCESS: Downloaded file: $TO_DOWNLOAD_URL"
}

remove_block() {
    # Clear everything in between
    # Dont redirect the output like >> or > it will wipe your file, edit in place
    sed "/$BLOCK_START/,/$BLOCK_END/d" $OUTPUT_FILE -i
    status "The block $COUNTRY_CODE removed" "Couldn't remove the block $COUNTRY_CODE"
}

insert_ips() {
    # Insert prefix before each line
    echo "$BLOCK_START" >> $OUTPUT_FILE
    sed "s/^/$PREFIX /" $INPUT_FILE >> $OUTPUT_FILE
    echo "$BLOCK_END" >> $OUTPUT_FILE
    echo "SUCCESS: Inserted IPs"
}

# Procceed only if 2 positional arguments are present
if has_arg "$1" "ALLOWED_ACTIONS" && has_arg "$2" "ALLOWED_CODES"; then
    if [ "$1" == "--add" ] || [ "$1" == "--update" ]; then
        download_the_ips
        remove_block
        insert_ips
        rm $INPUT_FILE
    elif [ "$1" == "--remove" ]; then
        remove_block
    fi
    exit 0
fi
exit 1
