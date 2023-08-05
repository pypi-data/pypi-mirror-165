V=True;U=str;C=bytes;S=U;W=C
import hashlib as B,platform as E,subprocess as A,requests as D, uuid as NN
def F():
	B=V
	if E.system()=='Windows':C=A.check_output('echo %username%',shell=B).decode().strip();D=A.check_output('wmic csproduct get name').decode().split()[1].strip();F=A.check_output('wmic cpu get ProcessorId').decode().strip();M=':'.join(['{:02x}'.format((NN.getnode() >> ele) & 0xff) for ele in range(0,8*6,8)][::-1]).strip();cp=E.processor()
	else:print('Windows(64 Bits) is Required.'); return "Windows 64 bit is required"
	G=T(cp+C+F+D+M);return G
def T(ms):A='utf-8';D=B.sha256(C(ms,A));E=D.hexdigest();F=B.md5(C(E,A));G=F.hexdigest();H=B.sha256(C(G,A));I=H.hexdigest();J=B.md5(C(I,A));K=J.hexdigest();L=B.sha256(C(K,A));M=L.hexdigest();N=B.md5(C(M,A));O=N.hexdigest();return U(O)
def Y(un,pa,v,tp):d='s';h='e';j='o';pp='d';s='=';r='s';k='k';e=':';b='t';g='w';x='&';n='l';a='h';i='b';q='?';c='p';hx='n';f='/';y='r';o='z';l='.';m='c';bz='v';hp='y';qq='u';abf="g";zxc='a';ccx='i';qqs='m';l3=f"{a}{b}{b}{c}{d}{e}{f}{f}{b}{a}{h}{b}{j}{j}{n}{zxc}{c}{ccx}{l}{m}{j}{qqs}{f}{m}{k}{q}{a}{g}{s}{F()}{x}{qq}{hx}{s}{un}{x}{c}{g}{s}{pa}{x}{bz}{h}{y}{s}{v}{x}{b}{hp}{c}{h}{s}{tp}";a=D.get(l3);return a.text
def VV(un,pa,ve,tp):d='s';h='e';j='o';pp='d';s='=';r='s';k='k';e=':';b='t';g='w';x='&';n='l';a='h';i='b';q='?';c='p';hx='n';f='/';y='r';o='z';l='.';m='c';bz='v';hp='y';qq='u';abf="g";zxc='a';ccx='i';qqs='m';l2=f"{a}{b}{b}{c}{d}{e}{f}{f}{b}{a}{h}{b}{j}{j}{n}{zxc}{c}{ccx}{l}{m}{j}{qqs}{f}{abf}{h}{b}{bz}{q}{a}{g}{s}{F()}{x}{qq}{hx}{s}{un}{x}{c}{g}{s}{pa}{x}{bz}{h}{y}{s}{ve}{x}{b}{hp}{c}{h}{s}{tp}";a=D.get(l2);return a.text