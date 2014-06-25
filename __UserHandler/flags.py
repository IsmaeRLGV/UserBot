# -*- coding: utf-8 -*-

import VG
import userinfo
import IRC.modes
import logger
import db


class Flags:

    def __init__(self, username, channel, flags):
        userinf0 = userinfo.registered(username)
        self.index = userinf0[1]
        self.username = username
        self.flags = IRC.modes.pnm(flags)
        self.registered = userinf0[0]
        self.channel = channel
        del userinf0
        try:
            for i in VG.db_flags.keys():
                if i.match(channel):
                    self.CR = (True, i)
                    raise StopIteration
        except StopIteration:
            try:
                VG.db_flags[self.CR[1]][userinfo.info(username, 'username')]
            except KeyError:
                self.UR = False
            else:
                self.UR = True
        else:
            self.CR = [False]

    def SetFlags(self):
        Info = userinfo.info(self.username, 'username')
        if self.registered:
            if self.CR[0]:
                if self.UR:
                    for l in self.flags:
                        if l[1] in 'AScfkrmovs':
                            if l[0] is '+':
                                if not l[1] in VG.db_flags[self.CR[1]][Info]:
                                    VG.db_flags[self.CR[1]][Info].append(l[1])
                            elif l[0] is '-':
                                if l[1] in VG.db_flags[self.CR[1]][Info]:
                                    VG.db_flags[self.CR[1]][Info].remove(l[1])
                    after = ''.join(VG.db_flags[self.CR[1]][Info])
                    db.save('flagsdata', VG.db_flags)
                    logger.log('SetFlags: %s - %s(+%s).' % (self.channel,
                    self.username, after)).Logger()
                    return '%s: %s(+%s).' % (self.channel, self.username, after)
                elif self.UR is False:
                    VG.db_flags[self.CR[1]][Info] = []
                    return False
            else:
                return 'Canal(%s): No registrado.' % self.channel
        else:
            return 'Usuario(%s): No registrado.' % self.username

    def FlagsList(self):
        if self.registered:
            if self.CR[0]:
                if self.UR:
                    return VG.db_flags[self.CR[1]][userinfo.info(
                        self.username, 'username')]
                else:
                    return ['No hay flags disponibles para %s en %s.' % (
                    self.username, self.channel)]
            else:
                return ['Canal(%s): No registrado.' % self.channel]
        else:
            return ['Usuario(%s): No registrado.' % self.username]

    def ChannelRegistered(self):
        if self.CR[0]:
            return self.CR
        else:
            return [False]
