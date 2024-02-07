from pprint import pprint

import polyline
import folium


encoded_polyline = "{y}cH_qzn@na@rw@tVuvA`QuhCjwAqjLlRksFz`AkuA|~AuuAns@o~Bl`Asy@t{@qnGfD_\\tk@moKia@icEin@apA`w@elBry@cvC}GotBnZyoKriA}`F}N}|FylAc_L{`BywDyi@{fFnBayLnk@ajFgAabEvIe}Ab~@cmBnrAahCbY_yCkCiqDpqCkdAxnFyeHdkBs|Ck^csByeA{|FufAq}LyN}_JppC{}JjvCyhIbpCgbEv{BowDn~@aeC~eB|A~zD_hHneB_yEfu@seCqC_}B{Z{`Eor@izGzaBwwFtTmnBrfAgcAhaCo|ExbC_rFfb@otG~xBezFrq@}uHiKksBtuBcDh{@bBbq@_vBthBs{AhjC~OdsA~bC~`Cvx@to@jqA|rDhSdcKjrJrrEhcE~dDxi@d_FiAl~AsI~zChu@rxA}eGnkBe`D|r@etEp_BalDzlAcxHdcDmuFup@a`Jr_BqgNb]_wHu`@{pJnb@}pC_b@ahBtHwxD`h@eoUuhBcnEaYimEqSovCaV_nG~`BqkDeNmbF`h@gnF{x@_~F}dDyyGubAw~DuhBc{DkiBsdGoe@goJyl@orD_AmiFsoAsbEurD{jIau@g{JywBkpM{fAkdJmH__E|kBg{D|aAizHnbBgnI}Co_JvhAgvEqEoeLc_Ah_@}Ola@kRi[tt@gqA}OqxAfn@hw@~]|eCveAntAd{D{hA`yBnGrq@~QqFwdAhyBwzCtiEacBdaCoMnsCoi@vt@kpAjlA{r@b~Cp_@pxAm}BpcBqpAbhC|gAj|CloExeGr_CpwAh}AhpBbGblDuoNfcBqjB~nDmbBxjBisJ`_CgzCbc@{fArzAmAxvDuq@zyCmZj{IjuJ`fFz{H`uI|uCxjC`qBvkBffBbgDxaIuLh|IdkAhtH`yCtdB~dCshAffCz{@dtH`kBhcFzoB|iH`fF~`D|wBrlB~|FbrBdeEzzBp`BpwBnkBhsEbjCnsDvBf{DsnBt~DwVlvCopApeEfHtvHvxBbaCvyDtpA~yExiD`sCnnGvgApuDyv@~~AkaAbuAdQlbFbfE|uBdmG`{MpkIbtIddHlgCtzEv`DjoAmC~o@bkAbp@zuCnx@h{Fff@viFp~Bzp@d~@}A~eClJ`v@oa@noOe}Dzfe@kaEbq[{gEnfUowBnrG|jAjxI`oBthZfuBtlKzYf_LfPhmIu~B~yK~_@hoJkPzzJnH`gN~ThlEbs@kJduArpAxuAeKuf@vhF{~@toBjFhxDha@fkHt]zqDxMnjDd^dsI"
decoded_polyline = polyline.decode(encoded_polyline)
map_route = folium.Map(
    location=[decoded_polyline[0][0], decoded_polyline[0][1]], zoom_start=10
)

folium.PolyLine(locations=decoded_polyline, color='blue').add_to(map_route)


if __name__ == "__main__":
    map_route.save('here_route_map.html')
    pprint(decoded_polyline)
