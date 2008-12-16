"""
    Plugin for streaming media from YleAreena (Finnish media portal)
"""

from string import *
import xbmcplugin
import sys, os.path
import urllib,urllib2
import xbmc, xbmcgui
import re, os, traceback
import cookielib, htmlentitydefs
import socket
import time, rfc822

# plugin constants
__plugin__ = "YleAreena"
__author__ = "doze"
__url__ = "http://code.google.com/p/doze-xbmc-plugins/"
__svn_url__ = "http://doze-xbmc-plugins.googlecode.com/svn/trunk/YleAreenaMusic"
__credits__ = "Team XBMC + All plugin developers"
__version__ = "1.0.1"

rootDir = xbmc.translatePath( os.path.join( os.getcwd().replace( ";", "" )))
cacheDir = os.path.join(rootDir, 'cache')
resDir = os.path.join(rootDir, 'resources')
imgDir = os.path.join(resDir, 'images')

urlopen = urllib2.urlopen
cj = cookielib.LWPCookieJar()
Request = urllib2.Request

if cj != None:
    if os.path.isfile(os.path.join(resDir, 'cookies.lwp')):
        cj.load(os.path.join(resDir, 'cookies.lwp'))
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    urllib2.install_opener(opener)

entitydefs = {
    'AElig':    u'\u00C6', # latin capital letter AE = latin capital ligature AE, U+00C6 ISOlat1'
    'Aacute':   u'\u00C1', # latin capital letter A with acute, U+00C1 ISOlat1'
    'Acirc':    u'\u00C2', # latin capital letter A with circumflex, U+00C2 ISOlat1'
    'Agrave':   u'\u00C0', # latin capital letter A with grave = latin capital letter A grave, U+00C0 ISOlat1'
    'Alpha':    u'\u0391', # greek capital letter alpha, U+0391'
    'Aring':    u'\u00C5', # latin capital letter A with ring above = latin capital letter A ring, U+00C5 ISOlat1'
    'Atilde':   u'\u00C3', # latin capital letter A with tilde, U+00C3 ISOlat1'
    'Auml':     u'\u00C4', # latin capital letter A with diaeresis, U+00C4 ISOlat1'
    'Beta':     u'\u0392', # greek capital letter beta, U+0392'
    'Ccedil':   u'\u00C7', # latin capital letter C with cedilla, U+00C7 ISOlat1'
    'Chi':      u'\u03A7', # greek capital letter chi, U+03A7'
    'Dagger':   u'\u2021', # double dagger, U+2021 ISOpub'
    'Delta':    u'\u0394', # greek capital letter delta, U+0394 ISOgrk3'
    'ETH':      u'\u00D0', # latin capital letter ETH, U+00D0 ISOlat1'
    'Eacute':   u'\u00C9', # latin capital letter E with acute, U+00C9 ISOlat1'
    'Ecirc':    u'\u00CA', # latin capital letter E with circumflex, U+00CA ISOlat1'
    'Egrave':   u'\u00C8', # latin capital letter E with grave, U+00C8 ISOlat1'
    'Epsilon':  u'\u0395', # greek capital letter epsilon, U+0395'
    'Eta':      u'\u0397', # greek capital letter eta, U+0397'
    'Euml':     u'\u00CB', # latin capital letter E with diaeresis, U+00CB ISOlat1'
    'Gamma':    u'\u0393', # greek capital letter gamma, U+0393 ISOgrk3'
    'Iacute':   u'\u00CD', # latin capital letter I with acute, U+00CD ISOlat1'
    'Icirc':    u'\u00CE', # latin capital letter I with circumflex, U+00CE ISOlat1'
    'Igrave':   u'\u00CC', # latin capital letter I with grave, U+00CC ISOlat1'
    'Iota':     u'\u0399', # greek capital letter iota, U+0399'
    'Iuml':     u'\u00CF', # latin capital letter I with diaeresis, U+00CF ISOlat1'
    'Kappa':    u'\u039A', # greek capital letter kappa, U+039A'
    'Lambda':   u'\u039B', # greek capital letter lambda, U+039B ISOgrk3'
    'Mu':       u'\u039C', # greek capital letter mu, U+039C'
    'Ntilde':   u'\u00D1', # latin capital letter N with tilde, U+00D1 ISOlat1'
    'Nu':       u'\u039D', # greek capital letter nu, U+039D'
    'OElig':    u'\u0152', # latin capital ligature OE, U+0152 ISOlat2'
    'Oacute':   u'\u00D3', # latin capital letter O with acute, U+00D3 ISOlat1'
    'Ocirc':    u'\u00D4', # latin capital letter O with circumflex, U+00D4 ISOlat1'
    'Ograve':   u'\u00D2', # latin capital letter O with grave, U+00D2 ISOlat1'
    'Omega':    u'\u03A9', # greek capital letter omega, U+03A9 ISOgrk3'
    'Omicron':  u'\u039F', # greek capital letter omicron, U+039F'
    'Oslash':   u'\u00D8', # latin capital letter O with stroke = latin capital letter O slash, U+00D8 ISOlat1'
    'Otilde':   u'\u00D5', # latin capital letter O with tilde, U+00D5 ISOlat1'
    'Ouml':     u'\u00D6', # latin capital letter O with diaeresis, U+00D6 ISOlat1'
    'Phi':      u'\u03A6', # greek capital letter phi, U+03A6 ISOgrk3'
    'Pi':       u'\u03A0', # greek capital letter pi, U+03A0 ISOgrk3'
    'Prime':    u'\u2033', # double prime = seconds = inches, U+2033 ISOtech'
    'Psi':      u'\u03A8', # greek capital letter psi, U+03A8 ISOgrk3'
    'Rho':      u'\u03A1', # greek capital letter rho, U+03A1'
    'Scaron':   u'\u0160', # latin capital letter S with caron, U+0160 ISOlat2'
    'Sigma':    u'\u03A3', # greek capital letter sigma, U+03A3 ISOgrk3'
    'THORN':    u'\u00DE', # latin capital letter THORN, U+00DE ISOlat1'
    'Tau':      u'\u03A4', # greek capital letter tau, U+03A4'
    'Theta':    u'\u0398', # greek capital letter theta, U+0398 ISOgrk3'
    'Uacute':   u'\u00DA', # latin capital letter U with acute, U+00DA ISOlat1'
    'Ucirc':    u'\u00DB', # latin capital letter U with circumflex, U+00DB ISOlat1'
    'Ugrave':   u'\u00D9', # latin capital letter U with grave, U+00D9 ISOlat1'
    'Upsilon':  u'\u03A5', # greek capital letter upsilon, U+03A5 ISOgrk3'
    'Uuml':     u'\u00DC', # latin capital letter U with diaeresis, U+00DC ISOlat1'
    'Xi':       u'\u039E', # greek capital letter xi, U+039E ISOgrk3'
    'Yacute':   u'\u00DD', # latin capital letter Y with acute, U+00DD ISOlat1'
    'Yuml':     u'\u0178', # latin capital letter Y with diaeresis, U+0178 ISOlat2'
    'Zeta':     u'\u0396', # greek capital letter zeta, U+0396'
    'aacute':   u'\u00E1', # latin small letter a with acute, U+00E1 ISOlat1'
    'acirc':    u'\u00E2', # latin small letter a with circumflex, U+00E2 ISOlat1'
    'acute':    u'\u00B4', # acute accent = spacing acute, U+00B4 ISOdia'
    'aelig':    u'\u00E6', # latin small letter ae = latin small ligature ae, U+00E6 ISOlat1'
    'agrave':   u'\u00E0', # latin small letter a with grave = latin small letter a grave, U+00E0 ISOlat1'
    'alefsym':  u'\u2135', # alef symbol = first transfinite cardinal, U+2135 NEW'
    'alpha':    u'\u03B1', # greek small letter alpha, U+03B1 ISOgrk3'
    'amp':      u'\u0026', # ampersand, U+0026 ISOnum'
    'and':      u'\u2227', # logical and = wedge, U+2227 ISOtech'
    'ang':      u'\u2220', # angle, U+2220 ISOamso'
    'aring':    u'\u00E5', # latin small letter a with ring above = latin small letter a ring, U+00E5 ISOlat1'
    'asymp':    u'\u2248', # almost equal to = asymptotic to, U+2248 ISOamsr'
    'atilde':   u'\u00E3', # latin small letter a with tilde, U+00E3 ISOlat1'
    'auml':     u'\u00E4', # latin small letter a with diaeresis, U+00E4 ISOlat1'
    'bdquo':    u'\u201E', # double low-9 quotation mark, U+201E NEW'
    'beta':     u'\u03B2', # greek small letter beta, U+03B2 ISOgrk3'
    'brvbar':   u'\u00A6', # broken bar = broken vertical bar, U+00A6 ISOnum'
    'bull':     u'\u2022', # bullet = black small circle, U+2022 ISOpub'
    'cap':      u'\u2229', # intersection = cap, U+2229 ISOtech'
    'ccedil':   u'\u00E7', # latin small letter c with cedilla, U+00E7 ISOlat1'
    'cedil':    u'\u00B8', # cedilla = spacing cedilla, U+00B8 ISOdia'
    'cent':     u'\u00A2', # cent sign, U+00A2 ISOnum'
    'chi':      u'\u03C7', # greek small letter chi, U+03C7 ISOgrk3'
    'circ':     u'\u02C6', # modifier letter circumflex accent, U+02C6 ISOpub'
    'clubs':    u'\u2663', # black club suit = shamrock, U+2663 ISOpub'
    'cong':     u'\u2245', # approximately equal to, U+2245 ISOtech'
    'copy':     u'\u00A9', # copyright sign, U+00A9 ISOnum'
    'crarr':    u'\u21B5', # downwards arrow with corner leftwards = carriage return, U+21B5 NEW'
    'cup':      u'\u222A', # union = cup, U+222A ISOtech'
    'curren':   u'\u00A4', # currency sign, U+00A4 ISOnum'
    'dArr':     u'\u21D3', # downwards double arrow, U+21D3 ISOamsa'
    'dagger':   u'\u2020', # dagger, U+2020 ISOpub'
    'darr':     u'\u2193', # downwards arrow, U+2193 ISOnum'
    'deg':      u'\u00B0', # degree sign, U+00B0 ISOnum'
    'delta':    u'\u03B4', # greek small letter delta, U+03B4 ISOgrk3'
    'diams':    u'\u2666', # black diamond suit, U+2666 ISOpub'
    'divide':   u'\u00F7', # division sign, U+00F7 ISOnum'
    'eacute':   u'\u00E9', # latin small letter e with acute, U+00E9 ISOlat1'
    'ecirc':    u'\u00EA', # latin small letter e with circumflex, U+00EA ISOlat1'
    'egrave':   u'\u00E8', # latin small letter e with grave, U+00E8 ISOlat1'
    'empty':    u'\u2205', # empty set = null set = diameter, U+2205 ISOamso'
    'emsp':     u'\u2003', # em space, U+2003 ISOpub'
    'ensp':     u'\u2002', # en space, U+2002 ISOpub'
    'epsilon':  u'\u03B5', # greek small letter epsilon, U+03B5 ISOgrk3'
    'equiv':    u'\u2261', # identical to, U+2261 ISOtech'
    'eta':      u'\u03B7', # greek small letter eta, U+03B7 ISOgrk3'
    'eth':      u'\u00F0', # latin small letter eth, U+00F0 ISOlat1'
    'euml':     u'\u00EB', # latin small letter e with diaeresis, U+00EB ISOlat1'
    'euro':     u'\u20AC', # euro sign, U+20AC NEW'
    'exist':    u'\u2203', # there exists, U+2203 ISOtech'
    'fnof':     u'\u0192', # latin small f with hook = function = florin, U+0192 ISOtech'
    'forall':   u'\u2200', # for all, U+2200 ISOtech'
    'frac12':   u'\u00BD', # vulgar fraction one half = fraction one half, U+00BD ISOnum'
    'frac14':   u'\u00BC', # vulgar fraction one quarter = fraction one quarter, U+00BC ISOnum'
    'frac34':   u'\u00BE', # vulgar fraction three quarters = fraction three quarters, U+00BE ISOnum'
    'frasl':    u'\u2044', # fraction slash, U+2044 NEW'
    'gamma':    u'\u03B3', # greek small letter gamma, U+03B3 ISOgrk3'
    'ge':       u'\u2265', # greater-than or equal to, U+2265 ISOtech'
    'gt':       u'\u003E', # greater-than sign, U+003E ISOnum'
    'hArr':     u'\u21D4', # left right double arrow, U+21D4 ISOamsa'
    'harr':     u'\u2194', # left right arrow, U+2194 ISOamsa'
    'hearts':   u'\u2665', # black heart suit = valentine, U+2665 ISOpub'
    'hellip':   u'\u2026', # horizontal ellipsis = three dot leader, U+2026 ISOpub'
    'iacute':   u'\u00ED', # latin small letter i with acute, U+00ED ISOlat1'
    'icirc':    u'\u00EE', # latin small letter i with circumflex, U+00EE ISOlat1'
    'iexcl':    u'\u00A1', # inverted exclamation mark, U+00A1 ISOnum'
    'igrave':   u'\u00EC', # latin small letter i with grave, U+00EC ISOlat1'
    'image':    u'\u2111', # blackletter capital I = imaginary part, U+2111 ISOamso'
    'infin':    u'\u221E', # infinity, U+221E ISOtech'
    'int':      u'\u222B', # integral, U+222B ISOtech'
    'iota':     u'\u03B9', # greek small letter iota, U+03B9 ISOgrk3'
    'iquest':   u'\u00BF', # inverted question mark = turned question mark, U+00BF ISOnum'
    'isin':     u'\u2208', # element of, U+2208 ISOtech'
    'iuml':     u'\u00EF', # latin small letter i with diaeresis, U+00EF ISOlat1'
    'kappa':    u'\u03BA', # greek small letter kappa, U+03BA ISOgrk3'
    'lArr':     u'\u21D0', # leftwards double arrow, U+21D0 ISOtech'
    'lambda':   u'\u03BB', # greek small letter lambda, U+03BB ISOgrk3'
    'lang':     u'\u2329', # left-pointing angle bracket = bra, U+2329 ISOtech'
    'laquo':    u'\u00AB', # left-pointing double angle quotation mark = left pointing guillemet, U+00AB ISOnum'
    'larr':     u'\u2190', # leftwards arrow, U+2190 ISOnum'
    'lceil':    u'\u2308', # left ceiling = apl upstile, U+2308 ISOamsc'
    'ldquo':    u'\u201C', # left double quotation mark, U+201C ISOnum'
    'le':       u'\u2264', # less-than or equal to, U+2264 ISOtech'
    'lfloor':   u'\u230A', # left floor = apl downstile, U+230A ISOamsc'
    'lowast':   u'\u2217', # asterisk operator, U+2217 ISOtech'
    'loz':      u'\u25CA', # lozenge, U+25CA ISOpub'
    'lrm':      u'\u200E', # left-to-right mark, U+200E NEW RFC 2070'
    'lsaquo':   u'\u2039', # single left-pointing angle quotation mark, U+2039 ISO proposed'
    'lsquo':    u'\u2018', # left single quotation mark, U+2018 ISOnum'
    'lt':       u'\u003C', # less-than sign, U+003C ISOnum'
    'macr':     u'\u00AF', # macron = spacing macron = overline = APL overbar, U+00AF ISOdia'
    'mdash':    u'\u2014', # em dash, U+2014 ISOpub'
    'micro':    u'\u00B5', # micro sign, U+00B5 ISOnum'
    'middot':   u'\u00B7', # middle dot = Georgian comma = Greek middle dot, U+00B7 ISOnum'
    'minus':    u'\u2212', # minus sign, U+2212 ISOtech'
    'mu':       u'\u03BC', # greek small letter mu, U+03BC ISOgrk3'
    'nabla':    u'\u2207', # nabla = backward difference, U+2207 ISOtech'
    'nbsp':     u'\u00A0', # no-break space = non-breaking space, U+00A0 ISOnum'
    'ndash':    u'\u2013', # en dash, U+2013 ISOpub'
    'ne':       u'\u2260', # not equal to, U+2260 ISOtech'
    'ni':       u'\u220B', # contains as member, U+220B ISOtech'
    'not':      u'\u00AC', # not sign, U+00AC ISOnum'
    'notin':    u'\u2209', # not an element of, U+2209 ISOtech'
    'nsub':     u'\u2284', # not a subset of, U+2284 ISOamsn'
    'ntilde':   u'\u00F1', # latin small letter n with tilde, U+00F1 ISOlat1'
    'nu':       u'\u03BD', # greek small letter nu, U+03BD ISOgrk3'
    'oacute':   u'\u00F3', # latin small letter o with acute, U+00F3 ISOlat1'
    'ocirc':    u'\u00F4', # latin small letter o with circumflex, U+00F4 ISOlat1'
    'oelig':    u'\u0153', # latin small ligature oe, U+0153 ISOlat2'
    'ograve':   u'\u00F2', # latin small letter o with grave, U+00F2 ISOlat1'
    'oline':    u'\u203E', # overline = spacing overscore, U+203E NEW'
    'omega':    u'\u03C9', # greek small letter omega, U+03C9 ISOgrk3'
    'omicron':  u'\u03BF', # greek small letter omicron, U+03BF NEW'
    'oplus':    u'\u2295', # circled plus = direct sum, U+2295 ISOamsb'
    'or':       u'\u2228', # logical or = vee, U+2228 ISOtech'
    'ordf':     u'\u00AA', # feminine ordinal indicator, U+00AA ISOnum'
    'ordm':     u'\u00BA', # masculine ordinal indicator, U+00BA ISOnum'
    'oslash':   u'\u00F8', # latin small letter o with stroke, = latin small letter o slash, U+00F8 ISOlat1'
    'otilde':   u'\u00F5', # latin small letter o with tilde, U+00F5 ISOlat1'
    'otimes':   u'\u2297', # circled times = vector product, U+2297 ISOamsb'
    'ouml':     u'\u00F6', # latin small letter o with diaeresis, U+00F6 ISOlat1'
    'para':     u'\u00B6', # pilcrow sign = paragraph sign, U+00B6 ISOnum'
    'part':     u'\u2202', # partial differential, U+2202 ISOtech'
    'permil':   u'\u2030', # per mille sign, U+2030 ISOtech'
    'perp':     u'\u22A5', # up tack = orthogonal to = perpendicular, U+22A5 ISOtech'
    'phi':      u'\u03C6', # greek small letter phi, U+03C6 ISOgrk3'
    'pi':       u'\u03C0', # greek small letter pi, U+03C0 ISOgrk3'
    'piv':      u'\u03D6', # greek pi symbol, U+03D6 ISOgrk3'
    'plusmn':   u'\u00B1', # plus-minus sign = plus-or-minus sign, U+00B1 ISOnum'
    'pound':    u'\u00A3', # pound sign, U+00A3 ISOnum'
    'prime':    u'\u2032', # prime = minutes = feet, U+2032 ISOtech'
    'prod':     u'\u220F', # n-ary product = product sign, U+220F ISOamsb'
    'prop':     u'\u221D', # proportional to, U+221D ISOtech'
    'psi':      u'\u03C8', # greek small letter psi, U+03C8 ISOgrk3'
    'quot':     u'\u0022', # quotation mark = APL quote, U+0022 ISOnum'
    'rArr':     u'\u21D2', # rightwards double arrow, U+21D2 ISOtech'
    'radic':    u'\u221A', # square root = radical sign, U+221A ISOtech'
    'rang':     u'\u232A', # right-pointing angle bracket = ket, U+232A ISOtech'
    'raquo':    u'\u00BB', # right-pointing double angle quotation mark = right pointing guillemet, U+00BB ISOnum'
    'rarr':     u'\u2192', # rightwards arrow, U+2192 ISOnum'
    'rceil':    u'\u2309', # right ceiling, U+2309 ISOamsc'
    'rdquo':    u'\u201D', # right double quotation mark, U+201D ISOnum'
    'real':     u'\u211C', # blackletter capital R = real part symbol, U+211C ISOamso'
    'reg':      u'\u00AE', # registered sign = registered trade mark sign, U+00AE ISOnum'
    'rfloor':   u'\u230B', # right floor, U+230B ISOamsc'
    'rho':      u'\u03C1', # greek small letter rho, U+03C1 ISOgrk3'
    'rlm':      u'\u200F', # right-to-left mark, U+200F NEW RFC 2070'
    'rsaquo':   u'\u203A', # single right-pointing angle quotation mark, U+203A ISO proposed'
    'rsquo':    u'\u2019', # right single quotation mark, U+2019 ISOnum'
    'sbquo':    u'\u201A', # single low-9 quotation mark, U+201A NEW'
    'scaron':   u'\u0161', # latin small letter s with caron, U+0161 ISOlat2'
    'sdot':     u'\u22C5', # dot operator, U+22C5 ISOamsb'
    'sect':     u'\u00A7', # section sign, U+00A7 ISOnum'
    'shy':      u'\u00AD', # soft hyphen = discretionary hyphen, U+00AD ISOnum'
    'sigma':    u'\u03C3', # greek small letter sigma, U+03C3 ISOgrk3'
    'sigmaf':   u'\u03C2', # greek small letter final sigma, U+03C2 ISOgrk3'
    'sim':      u'\u223C', # tilde operator = varies with = similar to, U+223C ISOtech'
    'spades':   u'\u2660', # black spade suit, U+2660 ISOpub'
    'sub':      u'\u2282', # subset of, U+2282 ISOtech'
    'sube':     u'\u2286', # subset of or equal to, U+2286 ISOtech'
    'sum':      u'\u2211', # n-ary sumation, U+2211 ISOamsb'
    'sup':      u'\u2283', # superset of, U+2283 ISOtech'
    'sup1':     u'\u00B9', # superscript one = superscript digit one, U+00B9 ISOnum'
    'sup2':     u'\u00B2', # superscript two = superscript digit two = squared, U+00B2 ISOnum'
    'sup3':     u'\u00B3', # superscript three = superscript digit three = cubed, U+00B3 ISOnum'
    'supe':     u'\u2287', # superset of or equal to, U+2287 ISOtech'
    'szlig':    u'\u00DF', # latin small letter sharp s = ess-zed, U+00DF ISOlat1'
    'tau':      u'\u03C4', # greek small letter tau, U+03C4 ISOgrk3'
    'there4':   u'\u2234', # therefore, U+2234 ISOtech'
    'theta':    u'\u03B8', # greek small letter theta, U+03B8 ISOgrk3'
    'thetasym': u'\u03D1', # greek small letter theta symbol, U+03D1 NEW'
    'thinsp':   u'\u2009', # thin space, U+2009 ISOpub'
    'thorn':    u'\u00FE', # latin small letter thorn with, U+00FE ISOlat1'
    'tilde':    u'\u02DC', # small tilde, U+02DC ISOdia'
    'times':    u'\u00D7', # multiplication sign, U+00D7 ISOnum'
    'trade':    u'\u2122', # trade mark sign, U+2122 ISOnum'
    'uArr':     u'\u21D1', # upwards double arrow, U+21D1 ISOamsa'
    'uacute':   u'\u00FA', # latin small letter u with acute, U+00FA ISOlat1'
    'uarr':     u'\u2191', # upwards arrow, U+2191 ISOnum'
    'ucirc':    u'\u00FB', # latin small letter u with circumflex, U+00FB ISOlat1'
    'ugrave':   u'\u00F9', # latin small letter u with grave, U+00F9 ISOlat1'
    'uml':      u'\u00A8', # diaeresis = spacing diaeresis, U+00A8 ISOdia'
    'upsih':    u'\u03D2', # greek upsilon with hook symbol, U+03D2 NEW'
    'upsilon':  u'\u03C5', # greek small letter upsilon, U+03C5 ISOgrk3'
    'uuml':     u'\u00FC', # latin small letter u with diaeresis, U+00FC ISOlat1'
    'weierp':   u'\u2118', # script capital P = power set = Weierstrass p, U+2118 ISOamso'
    'xi':       u'\u03BE', # greek small letter xi, U+03BE ISOgrk3'
    'yacute':   u'\u00FD', # latin small letter y with acute, U+00FD ISOlat1'
    'yen':      u'\u00A5', # yen sign = yuan sign, U+00A5 ISOnum'
    'yuml':     u'\u00FF', # latin small letter y with diaeresis, U+00FF ISOlat1'
    'zeta':     u'\u03B6', # greek small letter zeta, U+03B6 ISOgrk3'
    'zwj':      u'\u200D', # zero width joiner, U+200D NEW RFC 2070'
    'zwnj':     u'\u200C'  # zero width non-joiner, U+200C NEW RFC 2070'
}

entitydefs2 = {
    '$':    '%24',
    '&':    '%26',
    '+':    '%2B',
    ',':    '%2C',
    '/':    '%2F',
    ':':    '%3A',
    ';':    '%3B',
    '=':    '%3D',
    '?':    '%3F',
    '@':    '%40',
    ' ':    '%20',
    '"':    '%22',
    '<':    '%3C',
    '>':    '%3E',
    '#':    '%23',
    '%':    '%25',
    '{':    '%7B',
    '}':    '%7D',
    '|':    '%7C',
    '\\':   '%5C',
    '^':    '%5E',
    '~':    '%7E',
    '[':    '%5B',
    ']':    '%5D',
    '`':    '%60'
}

def clean1(s): # remove &XXX;
    if not s:
        return ''
    for name, value in entitydefs.iteritems():
        if u'&' in s:
            s = s.replace(u'&' + name + u';', value)
    return s;

def clean2(s): # remove \\uXXX
    pat = re.compile(r'\\u(....)')
    def sub(mo):
        return unichr(int(mo.group(1), 16))
    return pat.sub(sub, smart_unicode(s))

def clean3(s): # remove &#XXX;
    pat = re.compile(r'&#(\d+);')
    def sub(mo):
        return unichr(int(mo.group(1)))
    return decode(pat.sub(sub, smart_unicode(s)))

def clean4(s): # remove multiple '?'
    idx = s.rfind('?')
    if idx != -1:
        if s[:idx].rfind('?') != -1:
            s[idx] = '&'
            s = clean4(s)
    return s

def decode(s):
    if not s:
        return ''
    try:
        dic=htmlentitydefs.name2codepoint
        for key in dic.keys():
            entity='&' + key + ';'
            s=s.replace(entity, unichr(dic[key]))
    except:
        traceback.print_exc(file = sys.stdout)
    return s

def unquote_safe(s): # unquote
    if not s:
        return ''
    try:
        for key, value in entitydefs2.iteritems():
            s = s.replace(value, key)
    except:
        traceback.print_exc(file = sys.stdout)
    return s;

def quote_safe(s): # quote
    if not s:
        return ''
    try:
        for key, value in entitydefs2.iteritems():
            s = s.replace(key, value)
    except:
        traceback.print_exc(file = sys.stdout)
    return s;

def smart_unicode(s):
    if not s:
        return ''
    try:
        if not isinstance(s, basestring):
            if hasattr(s, '__unicode__'):
                s = unicode(s)
            else:
                s = unicode(str(s), 'UTF-8')
        elif not isinstance(s, unicode):
            s = unicode(s, 'UTF-8')
    except:
        if not isinstance(s, basestring):
            if hasattr(s, '__unicode__'):
                s = unicode(s)
            else:
                s = unicode(str(s), 'ISO-8859-1')
        elif not isinstance(s, unicode):
            s = unicode(s, 'ISO-8859-1')
    return s

def clean_name(s):
    if not s:
        return ''
    try:
        s = clean1(clean2(clean3(smart_unicode(s)))).replace('\r\n', '').replace('\n', '')
    except:
        traceback.print_exc(file = sys.stdout)
    return s

def clean_url(s):
    if not s:
        return ''
    try:
        s = clean4(s)
    except:
        traceback.print_exc(file = sys.stdout)
    return s

class YleAreena:

  def __init__(self):
    self.cookieJar = cookielib.CookieJar()

  def getKeyboard(self, default = "", heading = "", hidden = False):
    kboard = xbmc.Keyboard(default, heading, hidden)
    kboard.doModal()
    if (kboard.isConfirmed()):
        return urllib.quote_plus(kboard.getText())
    return default

  def openUrl(self, url):
    data=""
    # make the request
    try:
      request = Request(url)
      request.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')  
      cFile = opener.open(request)
      data = cFile.read()
      cFile.close()
    except Exception, value:
      dialog = xbmcgui.Dialog()
      dialog.ok("YleAreena - " +xbmc.getLocalizedString(257), 'URL:' +'\n'+ str(url) +'\n'+  'Exception:' +'\n'+ str(value) +'\n'+ 'Data:' +'\n'+ str(data))
    if (data==""):
      dialog = xbmcgui.Dialog()
      dialog.ok("YleAreena - " +xbmc.getLocalizedString(257), xbmc.getLocalizedString(284) +'\n'+ 'URL:' +'\n'+ str(url) +'\n'+ 'CookieJar:'+ str(self.cookieJar))
      return
    return data
  
  def browsePrograms(self, url):
    data = self.openUrl(url)
    #search and add programs
    rePattern = re.compile('<a href="/hae\?pid=([^\"]+)\">([^<]+)</a>[^>]+>[^>]+>[^>]+>[^>]+>[1-9]', re.IGNORECASE + re.DOTALL + re.MULTILINE)
    matches = rePattern.findall(data)
    for id, name in matches:
      liz=xbmcgui.ListItem(clean1(clean2(clean3(smart_unicode(name)))),iconImage="DefaultAudio.png")
      ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url = sys.argv[0] + "?action=browse_episodes&id="+id,listitem=liz,isFolder=True,totalItems=len(matches))
  
  def browsePodcasts(self, url):
    data = self.openUrl(url)
    #search and add programs
    rePattern = re.compile('<td class="product">(<a href="/hae\?pid=[^\"]+\">)?([^<]+)(</a>)?.*?podcast\"><a href=\"([^\"]+)', re.IGNORECASE + re.DOTALL + re.MULTILINE)
    matches = rePattern.findall(data)
    for notused1, name, notused2, url in matches:
        liz=xbmcgui.ListItem(clean1(clean2(clean3(smart_unicode(name)))),iconImage="DefaultAudio.png")
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url = sys.argv[0] + "?action=browse_podcast_episodes&url="+quote_safe(url),listitem=liz,isFolder=True,totalItems=len(matches))
                
  def browseEpisodes(self, url, showTitles = 0):
    data = self.openUrl(url)
    #check to see if search returned too many matches
    strre=re.compile('hakuosumia yli 100 kpl', re.IGNORECASE)
    m=strre.search(data)
    if m:
      dialog = xbmcgui.Dialog()
      dialog.ok("YleAreena", xbmc.getLocalizedString(30203))
      return
    #check to see if search didn't find any matches
    strre=re.compile('Ei ohjelmia annetuilla', re.IGNORECASE)
    m=strre.search(data)
    if m:
      dialog = xbmcgui.Dialog()
      dialog.ok("YleAreena", xbmc.getLocalizedString(30204))
      return
    #try to find more pages
    rePattern = re.compile('<a href="([^\"]+(.))\" class=\"next\"', re.IGNORECASE + re.DOTALL + re.MULTILINE)
    matches = rePattern.findall(data)
    nextpage = 0
    if (len(matches) > 0):
      nextpage = matches[0][1]
    #parse current page from url
    currentpage = 0
    pos = url.rfind('&s=')
    if (pos != -1):
      currentpage = url[pos+3:]
    #if more pages exists, make the link 
    if (nextpage > 1 and nextpage != currentpage):
      liz=xbmcgui.ListItem(xbmc.getLocalizedString(30200),iconImage="DefaultAudio.png", thumbnailImage=os.path.join(imgDir, 'next.png'))
      nextUrl = ''
      if (currentpage == 0):
        nextUrl = url + '&s=' + nextpage
      else:
        nextUrl = url[:pos+3] + nextpage
      ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url = sys.argv[0] + "?action=browse_episodes&nextUrl="+quote_safe(nextUrl),listitem=liz,isFolder=True)
    #search and add episodes            
    rePattern = re.compile('<a href=\"/toista\?id=([^\"]+)\"><img src=\"([^\"]+)\"[^a]+alt=\"([^\"]+)\".*?<a[^>]+>(.*?)<.*?time">(.{10,20})', re.IGNORECASE + re.DOTALL + re.MULTILINE)
    matches = rePattern.findall(data)
    for id, imgUrl, name, title, date in matches:
      if (showTitles == 1 and name != title):
        #strip ending dot from title, if it exists
        if (len(title) > 0): 
          if (title[len(title)-1] == '.'):
              title = title[0:len(title)-1]
          name = title + ': ' +name
      liz=xbmcgui.ListItem(clean1(clean2(clean3(smart_unicode(name)))),iconImage="DefaultAudio.png",thumbnailImage=imgUrl)
      liz.setInfo( "music", { "Title"        : clean1(clean2(clean3(smart_unicode(name)))),
                "Date"          : date[:2]+"-"+date[3:5]+"-"+date[6:10]
                })
      ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url = sys.argv[0] + "?action=play_episode&url="+quote_safe('http://www.yle.fi/java/areena/dispatcher/'+id+'.asx?bitrate=1000000'),listitem=liz,isFolder=False,totalItems=len(matches))
  
  def playEpisode(self, url):
    player = xbmc.Player( xbmc.PLAYER_CORE_MPLAYER ).play(url)
  
  def browsePodcastEpisodes(self, url):
    data = self.openUrl(url)
    #search and add programs
    rePattern = re.compile('<item.*?<title>(.*?)</title>.*?enclosure url="([^\"]+).*?<pubdate>(.*?)</pubdate>', re.IGNORECASE + re.DOTALL + re.MULTILINE)
    matches = rePattern.findall(data)
    for name, url, pubdate in matches:
        liz=xbmcgui.ListItem(clean1(clean2(clean3(smart_unicode(name)))),iconImage="DefaultAudio.png")
        #try parsing a date for the podcast items
        try:
            timestamp = rfc822.mktime_tz(rfc822.parsedate_tz(pubdate))
            liz.setInfo( "music", { "Title"        : clean1(clean2(clean3(smart_unicode(name)))),
                "Date"          : time.strftime ("%d-%m-%Y", time.localtime (timestamp))
                })
        except:
            traceback.print_exc(file = sys.stdout)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url = sys.argv[0] + "?action=play_episode&url="+quote_safe(url),listitem=liz,isFolder=False,totalItems=len(matches))
         
  def doSearch(self):
    #open keyboard with last search entry, if exists
    try:
      f = open(os.path.join(cacheDir, 'search'), 'r')
      curr_phrase = urllib.unquote_plus(f.read())
      f.close()
    except:
      curr_phrase = ''
    search_phrase = self.getKeyboard(default = clean1(clean2(clean3(smart_unicode(curr_phrase)))), heading = xbmc.getLocalizedString(30102))
    xbmc.sleep(10)
    f = open(os.path.join(cacheDir, 'search'), 'w')
    f.write(search_phrase)
    f.close()
    #show episodes matching keyword
    self.browseEpisodes('http://areena.yle.fi/hae?keyword='+search_phrase+'&filter=1,2', 1)
  
#main logic
y=YleAreena()

#parse parameters
params = sys.argv[2]
param = {}
if (params != ""):
  cleanedparams = params.replace('?', '')
  if (params[len(params)-1] == '/'):
      params = params[0:len(params)-2]
  pairsofparams = cleanedparams.split('&')
  for i in range(len(pairsofparams)):
      splitparams = {}
      splitparams = pairsofparams[i].split('=')
      if (len(splitparams)) == 2:
          param[splitparams[0]] = splitparams[1]

if (params != ""):
  #browse programs
  if (urllib.unquote_plus(param['action']) == "browse_programs"):
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )
    y.browsePrograms('http://areena.yle.fi/selaa')
  #browse podcasts
  elif (urllib.unquote_plus(param['action']) == "browse_podcasts"):
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )
    y.browsePodcasts('http://areena.yle.fi/podcast')
  #browse podcast episodes
  elif (urllib.unquote_plus(param['action']) == "browse_podcast_episodes"):
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_DATE )
    url = param.get('url', '')
    if (url != ''):
        y.browsePodcastEpisodes(unquote_safe(url))
  #browse episodes
  elif (urllib.unquote_plus(param['action']) == "browse_episodes"):
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_DATE )
    id = param.get('id', '')
    nextUrl = param.get('nextUrl', '')
    #if id is given, display first page
    if (id != ''):
      y.browseEpisodes('http://areena.yle.fi/hae?pid='+id+'&filter=1,2')
    #if nextUrl is given, display that page
    elif (nextUrl != ''):
      y.browseEpisodes(unquote_safe(nextUrl),1)
  #do search
  elif (urllib.unquote_plus(param['action']) == "search"):
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_DATE )
    y.doSearch()
  elif (urllib.unquote_plus(param['action']) == "play_episode"):
    url = param.get('url', '')
    if (url != ''):
      y.playEpisode(unquote_safe(url))
  elif (urllib.unquote_plus(param['action']) == "browse_live"):
    liz=xbmcgui.ListItem(xbmc.getLocalizedString(30217),iconImage="DefaultAudio.png")
    ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = 'http://www.yle.fi/elavaarkisto/nettiradio.asx', listitem = liz, isFolder = False)
    liz=xbmcgui.ListItem(xbmc.getLocalizedString(30218),iconImage="DefaultAudio.png")
    ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = 'http://yle.fi/livestream/yleradio1.asx', listitem = liz, isFolder = False)
    liz=xbmcgui.ListItem(xbmc.getLocalizedString(30219),iconImage="DefaultAudio.png")
    ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = 'http://akastreaming.yle.fi/vp/fiyle/no_geo/live_f.asx', listitem = liz, isFolder = False)
    liz=xbmcgui.ListItem(xbmc.getLocalizedString(30220),iconImage="DefaultAudio.png")
    ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = 'http://www.yle.fi/livestream/radiosuomi.asx', listitem = liz, isFolder = False)
    liz=xbmcgui.ListItem(xbmc.getLocalizedString(30221),iconImage="DefaultAudio.png")
    ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = 'http://www.yle.fi/peili/peili.asx', listitem = liz, isFolder = False)
    liz=xbmcgui.ListItem(xbmc.getLocalizedString(30222),iconImage="DefaultAudio.png")
    ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = 'http://yle.fi/livestream/ylenklassinen.asx', listitem = liz, isFolder = False)
    liz=xbmcgui.ListItem(xbmc.getLocalizedString(30223),iconImage="DefaultAudio.png")
    ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = 'http://yle.fi/livestream/vega.asx', listitem = liz, isFolder = False)
    liz=xbmcgui.ListItem(xbmc.getLocalizedString(30224),iconImage="DefaultAudio.png")
    ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = 'http://yle.fi/livestream/x3m.asx', listitem = liz, isFolder = False)
    liz=xbmcgui.ListItem(xbmc.getLocalizedString(30225),iconImage="DefaultAudio.png")
    ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = 'http://yle.fi/livestream/samiradio.asx', listitem = liz, isFolder = False)
    liz=xbmcgui.ListItem(xbmc.getLocalizedString(30226),iconImage="DefaultAudio.png")
    ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = 'http://yle.fi/livestream/etelakarjala.asx', listitem = liz, isFolder = False)
    liz=xbmcgui.ListItem(xbmc.getLocalizedString(30227),iconImage="DefaultAudio.png")
    ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = 'http://yle.fi/livestream/etelasavo.asx', listitem = liz, isFolder = False)
    liz=xbmcgui.ListItem(xbmc.getLocalizedString(30228),iconImage="DefaultAudio.png")
    ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = 'http://yle.fi/livestream/radiohame.asx', listitem = liz, isFolder = False)
    liz=xbmcgui.ListItem(xbmc.getLocalizedString(30229),iconImage="DefaultAudio.png")
    ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = 'http://yle.fi/livestream/itauusimaa.asx', listitem = liz, isFolder = False)
    liz=xbmcgui.ListItem(xbmc.getLocalizedString(30230),iconImage="DefaultAudio.png")
    ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = 'http://yle.fi/livestream/kainuu.asx', listitem = liz, isFolder = False)
    liz=xbmcgui.ListItem(xbmc.getLocalizedString(30231),iconImage="DefaultAudio.png")
    ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = 'http://yle.fi/livestream/keskipohjanmaa.asx', listitem = liz, isFolder = False)
    liz=xbmcgui.ListItem(xbmc.getLocalizedString(30232),iconImage="DefaultAudio.png")
    ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = 'http://yle.fi/livestream/keskisuomi.asx', listitem = liz, isFolder = False)
    liz=xbmcgui.ListItem(xbmc.getLocalizedString(30233),iconImage="DefaultAudio.png")
    ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = 'http://yle.fi/livestream/kymenlaakso.asx', listitem = liz, isFolder = False)
    liz=xbmcgui.ListItem(xbmc.getLocalizedString(30234),iconImage="DefaultAudio.png")
    ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = 'http://yle.fi/livestream/lapinradio.asx', listitem = liz, isFolder = False)
    liz=xbmcgui.ListItem(xbmc.getLocalizedString(30235),iconImage="DefaultAudio.png")
    ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = 'http://yle.fi/livestream/perameri.asx', listitem = liz, isFolder = False)
    liz=xbmcgui.ListItem(xbmc.getLocalizedString(30236),iconImage="DefaultAudio.png")
    ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = 'http://yle.fi/livestream/ylenlantinen.asx', listitem = liz, isFolder = False)
    liz=xbmcgui.ListItem(xbmc.getLocalizedString(30237),iconImage="DefaultAudio.png")
    ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = 'http://yle.fi/livestream/tampere.asx', listitem = liz, isFolder = False)
    liz=xbmcgui.ListItem(xbmc.getLocalizedString(30238),iconImage="DefaultAudio.png")
    ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = 'http://yle.fi/livestream/pohjanmaa.asx', listitem = liz, isFolder = False)
    liz=xbmcgui.ListItem(xbmc.getLocalizedString(30239),iconImage="DefaultAudio.png")
    ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = 'http://yle.fi/livestream/pohjkarjala.asx', listitem = liz, isFolder = False)
    liz=xbmcgui.ListItem(xbmc.getLocalizedString(30240),iconImage="DefaultAudio.png")
    ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = 'http://yle.fi/livestream/ouluradio.asx', listitem = liz, isFolder = False)
    liz=xbmcgui.ListItem(xbmc.getLocalizedString(30241),iconImage="DefaultAudio.png")
    ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = 'http://yle.fi/livestream/radiosavo.asx', listitem = liz, isFolder = False)
    liz=xbmcgui.ListItem(xbmc.getLocalizedString(30242),iconImage="DefaultAudio.png")
    ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = 'http://yle.fi/livestream/lahdenradio.asx', listitem = liz, isFolder = False)
    liz=xbmcgui.ListItem(xbmc.getLocalizedString(30243),iconImage="DefaultAudio.png")
    ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = 'http://yle.fi/livestream/radiosuomi.asx', listitem = liz, isFolder = False)
    liz=xbmcgui.ListItem(xbmc.getLocalizedString(30244),iconImage="DefaultAudio.png")
    ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = 'http://yle.fi/livestream/satakunta.asx', listitem = liz, isFolder = False)
    liz=xbmcgui.ListItem(xbmc.getLocalizedString(30245),iconImage="DefaultAudio.png")
    ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = 'http://yle.fi/livestream/turunradio.asx', listitem = liz, isFolder = False)
    liz=xbmcgui.ListItem(xbmc.getLocalizedString(30246),iconImage="DefaultAudio.png")
    ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = 'http://yle.fi/livestream/vegaoster.asx', listitem = liz, isFolder = False)
    liz=xbmcgui.ListItem(xbmc.getLocalizedString(30247),iconImage="DefaultAudio.png")
    ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = 'http://yle.fi/livestream/vegaabo.asx', listitem = liz, isFolder = False)
    liz=xbmcgui.ListItem(xbmc.getLocalizedString(30248),iconImage="DefaultAudio.png")
    ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = 'http://yle.fi/livestream/vegavast.asx', listitem = liz, isFolder = False)
    liz=xbmcgui.ListItem(xbmc.getLocalizedString(30249),iconImage="DefaultAudio.png")
    ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = 'http://yle.fi/livestream/vega.asx', listitem = liz, isFolder = False)
    liz=xbmcgui.ListItem(xbmc.getLocalizedString(30250),iconImage="DefaultAudio.png")
    ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = 'http://yle.fi/livestream/vegaost.asx', listitem = liz, isFolder = False)
  #pre-set categories
  elif (urllib.unquote_plus(param['action']) == "browse_news"):
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_DATE )
    y.browseEpisodes('http://areena.yle.fi/hae?cid=164618&filter=1,2', 1)
  elif (urllib.unquote_plus(param['action']) == "browse_sports"):
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_DATE )
    y.browseEpisodes('http://areena.yle.fi/hae?cid=164619&filter=1,2', 1)
  elif (urllib.unquote_plus(param['action']) == "browse_current"):
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_DATE )
    y.browseEpisodes('http://areena.yle.fi/hae?cid=164612&filter=1,2', 1)
  elif (urllib.unquote_plus(param['action']) == "browse_documentaries"):
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_DATE )
    y.browseEpisodes('http://areena.yle.fi/hae?cid=164620&filter=1,2', 1)
  elif (urllib.unquote_plus(param['action']) == "browse_learning"):
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_DATE )
    y.browseEpisodes('http://areena.yle.fi/hae?cid=164621&filter=1,2', 1)
  elif (urllib.unquote_plus(param['action']) == "browse_culture"):
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_DATE )
    y.browseEpisodes('http://areena.yle.fi/hae?cid=164622&filter=1,2', 1)
  elif (urllib.unquote_plus(param['action']) == "browse_entertainment"):
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_DATE )
    y.browseEpisodes('http://areena.yle.fi/hae?cid=164560&filter=1,2', 1)
  elif (urllib.unquote_plus(param['action']) == "browse_music"):
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_DATE )
    y.browseEpisodes('http://areena.yle.fi/hae?cid=164623&filter=1,2', 1)
  elif (urllib.unquote_plus(param['action']) == "browse_drama"):
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_DATE )
    y.browseEpisodes('http://areena.yle.fi/hae?cid=164550&filter=1,2', 1)
  elif (urllib.unquote_plus(param['action']) == "browse_children"):
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_DATE )
    y.browseEpisodes('http://areena.yle.fi/hae?cid=164553&filter=1,2', 1)
  elif (urllib.unquote_plus(param['action']) == "browse_areas"):
    liz=xbmcgui.ListItem(xbmc.getLocalizedString(30207),iconImage="DefaultAudio.png")
    ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = sys.argv[0] + "?action=browse_news", listitem = liz, isFolder = True)
    liz=xbmcgui.ListItem(xbmc.getLocalizedString(30208),iconImage="DefaultAudio.png")
    ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = sys.argv[0] + "?action=browse_sports", listitem = liz, isFolder = True)
    liz=xbmcgui.ListItem(xbmc.getLocalizedString(30209),iconImage="DefaultAudio.png")
    ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = sys.argv[0] + "?action=browse_current", listitem = liz, isFolder = True)
    liz=xbmcgui.ListItem(xbmc.getLocalizedString(30210),iconImage="DefaultAudio.png")
    ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = sys.argv[0] + "?action=browse_documentaries", listitem = liz, isFolder = True)
    liz=xbmcgui.ListItem(xbmc.getLocalizedString(30211),iconImage="DefaultAudio.png")
    ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = sys.argv[0] + "?action=browse_learning", listitem = liz, isFolder = True)
    liz=xbmcgui.ListItem(xbmc.getLocalizedString(30212),iconImage="DefaultAudio.png")
    ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = sys.argv[0] + "?action=browse_culture", listitem = liz, isFolder = True)
    liz=xbmcgui.ListItem(xbmc.getLocalizedString(30213),iconImage="DefaultAudio.png")
    ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = sys.argv[0] + "?action=browse_entertainment", listitem = liz, isFolder = True)
    liz=xbmcgui.ListItem(xbmc.getLocalizedString(30214),iconImage="DefaultAudio.png")
    ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = sys.argv[0] + "?action=browse_music", listitem = liz, isFolder = True)
    liz=xbmcgui.ListItem(xbmc.getLocalizedString(30215),iconImage="DefaultAudio.png")
    ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = sys.argv[0] + "?action=browse_drama", listitem = liz, isFolder = True)
    liz=xbmcgui.ListItem(xbmc.getLocalizedString(30216),iconImage="DefaultAudio.png")
    ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = sys.argv[0] + "?action=browse_children", listitem = liz, isFolder = True)
  
#no parameters set, open default view
else:
  liz=xbmcgui.ListItem(xbmc.getLocalizedString(30201),iconImage="DefaultAudio.png")
  ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = sys.argv[0] + "?action=browse_programs", listitem = liz, isFolder = True)
  liz=xbmcgui.ListItem(xbmc.getLocalizedString(30202),iconImage="DefaultAudio.png")
  ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = sys.argv[0] + "?action=search", listitem = liz, isFolder = True)
  liz=xbmcgui.ListItem(xbmc.getLocalizedString(30205),iconImage="DefaultAudio.png")
  ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = sys.argv[0] + "?action=browse_podcasts", listitem = liz, isFolder = True)
  liz=xbmcgui.ListItem(xbmc.getLocalizedString(30206),iconImage="DefaultAudio.png")
  ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = sys.argv[0] + "?action=browse_live", listitem = liz, isFolder = True)  
  liz=xbmcgui.ListItem(xbmc.getLocalizedString(30251),iconImage="DefaultAudio.png")
  ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = sys.argv[0] + "?action=browse_areas", listitem = liz, isFolder = True)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
