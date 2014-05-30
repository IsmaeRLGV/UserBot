# -*- coding: utf-8 -*-

def pnm(m_str):
	return _pn(m_str, "")
	
def pcm(m_str):
	return _pn(m_str, "bklvohq")
	
def _pn(m_str, unary_modes=""):
	if not m_str or not m_str[0] in '+-':
		return []
	modes = []
	parts = m_str.split()
	mode_part, args = parts[0], parts[1:]
	for ch in mode_part:
		if ch in "+-":
			sign = ch
			continue
		arg = args.pop(0) if ch in unary_modes and args else None
		modes.append([sign, ch, arg])
	return modes
