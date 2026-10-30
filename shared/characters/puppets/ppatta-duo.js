// 빠따 만화 캐릭터 두 명(수험생, 민트 토끼)을 코드로 다시 그린 인형.
// 원본: shared/keyvisuals/ppatta-comic-sqld-01.png (상반신만 있어 전신은 그림체를 따라 새로 그림).
// 쓰는 법: <svg viewBox="0 0 400 600">${PPATTA.student("id")}</svg> → 부위별 g에 id-legL, id-armR, id-head 등이 붙는다.
// 관절 기준점(GSAP svgOrigin): 다리 위쪽, 어깨, 목. PPATTA.pivots 참고. 발끝 기준선 y=562.
(function () {
  const INK = "#2B2B3A", SW = 7;
  const S = `stroke="${INK}" stroke-width="${SW}" stroke-linejoin="round" stroke-linecap="round"`;
  const C = {
    skin: "#FCE3CF", cheek: "#F6A7A7", hair: "#A25A30", hairHi: "#C47A47",
    hoodie: "#2F3F92", hoodieDark: "#26357E", hood: "#3B50A6", string: "#F4F4F4",
    pants: "#4B4F5E", shoe: "#F5F5F5", sole: "#C9CCD3",
    mint: "#8FD4C4", mintDark: "#77C2B1", face: "#FFFFFF", rCheek: "#F7B3C4", mouth: "#5B2A33", tongue: "#F08FA0",
  };

  function student(id) {
    return `
<g id="${id}">
  <g id="${id}-legL">
    <path d="M152,416 L192,416 L190,536 L154,536 Z" fill="${C.pants}" ${S}/>
    <path d="M146,532 Q144,562 166,563 L200,563 Q208,548 192,532 Z" fill="${C.shoe}" ${S}/>
  </g>
  <g id="${id}-legR">
    <path d="M208,416 L248,416 L246,536 L210,536 Z" fill="${C.pants}" ${S}/>
    <path d="M208,532 Q192,548 200,563 L234,563 Q256,562 254,532 Z" fill="${C.shoe}" ${S}/>
  </g>
  <g id="${id}-body">
    <path d="M128,302 Q130,258 166,250 L234,250 Q270,258 272,302 L280,418 Q280,432 266,432 L134,432 Q120,432 120,418 Z" fill="${C.hoodie}" ${S}/>
    <path d="M156,372 Q200,364 244,372 L249,414 L151,414 Z" fill="${C.hoodieDark}" stroke="${INK}" stroke-width="5" stroke-linejoin="round"/>
    <path d="M140,262 Q200,304 260,262 Q262,246 250,240 L150,240 Q138,246 140,262 Z" fill="${C.hood}" ${S}/>
    <path d="M184,272 L181,312 M216,272 L219,312" stroke="${C.string}" stroke-width="6" stroke-linecap="round"/>
    <circle cx="181" cy="316" r="5" fill="${C.string}" stroke="${INK}" stroke-width="3"/>
    <circle cx="219" cy="316" r="5" fill="${C.string}" stroke="${INK}" stroke-width="3"/>
  </g>
  <g id="${id}-armL">
    <path d="M140,268 Q108,276 104,326 L98,392 Q98,406 112,406 L132,404 Q134,352 146,300 Z" fill="${C.hoodie}" ${S}/>
    <circle cx="114" cy="411" r="18" fill="${C.skin}" ${S}/>
  </g>
  <g id="${id}-armR">
    <path d="M260,268 Q292,276 296,326 L302,392 Q302,406 288,406 L268,404 Q266,352 254,300 Z" fill="${C.hoodie}" ${S}/>
    <circle cx="286" cy="411" r="18" fill="${C.skin}" ${S}/>
  </g>
  <g id="${id}-head">
    <circle cx="104" cy="194" r="17" fill="${C.skin}" ${S}/>
    <circle cx="296" cy="194" r="17" fill="${C.skin}" ${S}/>
    <ellipse cx="200" cy="164" rx="98" ry="92" fill="${C.skin}" ${S}/>
    <path d="M100,182 Q82,72 200,54 Q318,72 300,182 Q298,198 290,204 Q292,172 282,152 Q274,170 260,162 Q262,138 244,130 Q238,152 220,154 Q216,128 196,124 Q190,150 172,152 Q166,128 150,132 Q150,156 132,160 Q124,150 118,152 Q110,174 112,204 Q102,196 100,182 Z" fill="${C.hair}" ${S}/>
    <path d="M196,58 Q204,26 228,38 Q210,44 208,60" fill="${C.hair}" ${S}/>
    <path d="M138,90 Q168,72 202,72" fill="none" stroke="${C.hairHi}" stroke-width="7" stroke-linecap="round"/>
    <g id="${id}-face">
      <ellipse cx="166" cy="186" rx="8" ry="11" fill="${INK}"/>
      <ellipse cx="234" cy="186" rx="8" ry="11" fill="${INK}"/>
      <circle cx="169" cy="182" r="3" fill="#FFF"/>
      <circle cx="237" cy="182" r="3" fill="#FFF"/>
      <ellipse cx="146" cy="210" rx="15" ry="9" fill="${C.cheek}" opacity="0.55"/>
      <ellipse cx="254" cy="210" rx="15" ry="9" fill="${C.cheek}" opacity="0.55"/>
      <path id="${id}-mouth" d="M186,214 Q200,230 214,214 Z" fill="${C.mouth}" stroke="${INK}" stroke-width="4" stroke-linejoin="round"/>
    </g>
  </g>
</g>`;
  }

  function rabbit(id) {
    return `
<g id="${id}">
  <g id="${id}-legL">
    <path d="M150,452 L192,452 L190,540 Q190,563 168,563 Q146,563 146,540 Z" fill="${C.mint}" ${S}/>
  </g>
  <g id="${id}-legR">
    <path d="M208,452 L250,452 L254,540 Q254,563 232,563 Q210,563 210,540 Z" fill="${C.mint}" ${S}/>
  </g>
  <g id="${id}-body">
    <path d="M132,322 Q200,300 268,322 L284,446 Q284,468 262,468 L138,468 Q116,468 116,446 Z" fill="${C.mint}" ${S}/>
    <path d="M168,330 Q200,322 232,330" fill="none" stroke="${C.mintDark}" stroke-width="6" stroke-linecap="round"/>
  </g>
  <g id="${id}-armL">
    <path d="M142,334 Q106,352 102,410 Q102,424 118,424 Q134,424 136,410 L154,358 Z" fill="${C.mint}" ${S}/>
    <circle cx="119" cy="426" r="19" fill="#FFFFFF" ${S}/>
  </g>
  <g id="${id}-armR">
    <path d="M258,334 Q294,352 298,410 Q298,424 282,424 Q266,424 264,410 L246,358 Z" fill="${C.mint}" ${S}/>
    <circle cx="281" cy="426" r="19" fill="#FFFFFF" ${S}/>
  </g>
  <g id="${id}-head">
    <g id="${id}-earL"><path d="M138,160 Q104,46 148,22 Q186,28 184,150 Z" fill="${C.mint}" ${S}/></g>
    <g id="${id}-earR"><path d="M262,160 Q296,46 252,22 Q214,28 216,150 Z" fill="${C.mint}" ${S}/></g>
    <circle cx="200" cy="232" r="112" fill="${C.mint}" ${S}/>
    <ellipse cx="200" cy="246" rx="80" ry="72" fill="${C.face}" stroke="${INK}" stroke-width="5"/>
    <g id="${id}-face">
      <ellipse cx="176" cy="238" rx="7" ry="10" fill="${INK}"/>
      <ellipse cx="224" cy="238" rx="7" ry="10" fill="${INK}"/>
      <ellipse cx="152" cy="264" rx="16" ry="11" fill="${C.rCheek}" opacity="0.85"/>
      <ellipse cx="248" cy="264" rx="16" ry="11" fill="${C.rCheek}" opacity="0.85"/>
      <path id="${id}-mouth" d="M186,262 Q200,288 214,262 Z" fill="${C.mouth}" stroke="${INK}" stroke-width="4" stroke-linejoin="round"/>
      <path d="M192,274 Q200,282 208,274" fill="${C.tongue}"/>
    </g>
  </g>
</g>`;
  }

  window.PPATTA = {
    student, rabbit, colors: C,
    pivots: {
      student: { legL: "172 418", legR: "228 418", armL: "138 280", armR: "262 280", head: "200 252", body: "200 432" },
      rabbit: { legL: "170 454", legR: "230 454", armL: "142 340", armR: "258 340", head: "200 330", body: "200 468", earL: "160 150", earR: "240 150" },
    },
  };
})();
