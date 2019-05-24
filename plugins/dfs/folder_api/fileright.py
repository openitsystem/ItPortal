# -*- coding: utf-8 -*-
'''
Manage DACLs on Windows

:depends:   - winreg Python module
'''

# Import python libs
from __future__ import absolute_import
import os
import logging
import re

# TODO: Figure out the exceptions that could be raised and properly catch
#       them instead of a bare except that catches any exception at all
#       may also need to add the ability to take ownership of an object to set
#       permissions if the minion is running as a user and not LOCALSYSTEM

# Import salt libs


import win32security
import ntsecuritycon

HAS_WINDOWS_MODULES = True

log = logging.getLogger(__name__)

# Define the module's virtual name
__virtualname__ = 'win_dacl'


class daclConstants(object):
    '''
    DACL constants used throughout the module  整个模块使用DACL常数
    '''
    # Definition in ntsecuritycon is incorrect (does not match winnt.h). The version在ntsecuritycon
    # #定义是不正确的（不匹配的。H）。版本
    #在ntsecuritycon有额外的位元0x200启用。
    #注意你当你设置这个权限你通常会回到它
    #或与0x200（si_no_acl_protect），这是什么ntsecuritycon错误定义。
    # in ntsecuritycon has the extra bits 0x200 enabled.
    # Note that you when you set this permission what you'll generally get back is it
    # ORed with 0x200 (SI_NO_ACL_PROTECT), which is what ntsecuritycon incorrectly defines.

    def __init__(self):
        self.FILE_ALL_ACCESS = (ntsecuritycon.STANDARD_RIGHTS_REQUIRED | ntsecuritycon.SYNCHRONIZE | 0x1ff)

        self.hkeys_security = {
            'HKEY_LOCAL_MACHINE': 'MACHINE',
            'HKEY_USERS': 'USERS',
            'HKEY_CURRENT_USER': 'CURRENT_USER',
            'HKEY_CLASSES_ROOT': 'CLASSES_ROOT',
            'MACHINE': 'MACHINE',
            'USERS': 'USERS',
            'CURRENT_USER': 'CURRENT_USER',
            'CLASSES_ROOT': 'CLASSES_ROOT',
            'HKLM': 'MACHINE',
            'HKU': 'USERS',
            'HKCU': 'CURRENT_USER',
            'HKCR': 'CLASSES_ROOT',
            }
        self.rights = {
            win32security.SE_FILE_OBJECT: {
                'READ': {
                    'BITS': ntsecuritycon.FILE_GENERIC_READ,
                    'TEXT': 'read'},
                'WRITE': {
                    'BITS': ntsecuritycon.FILE_GENERIC_WRITE,
                    'TEXT': 'write'},
                'READ&EXECUTE': {
                    'BITS': ntsecuritycon.FILE_GENERIC_EXECUTE |
                    ntsecuritycon.FILE_GENERIC_READ,
                    'TEXT': 'read and execute'},#读取和执行
                'MODIFY': {
                    'BITS': ntsecuritycon.FILE_GENERIC_WRITE |
                    ntsecuritycon.FILE_GENERIC_READ |
                    ntsecuritycon.FILE_GENERIC_EXECUTE |
                    ntsecuritycon.DELETE,
                    'TEXT': 'modify'}, #修改
                'FULLCONTROL': {
                    'BITS': self.FILE_ALL_ACCESS,
                    'TEXT': 'full control'}#完全控制
            }
        }
        self.validAceTypes = {
            'ALLOW': {'TEXT': 'allowed', 'BITS': 0},
            'DENY': {'TEXT': 'denied', 'BITS': 1}}
        self.validPropagations = {
            win32security.SE_REGISTRY_KEY: {
                'KEY': {
                    'TEXT': 'this key only',
                    'BITS': win32security.NO_INHERITANCE},
                'KEY&SUBKEYS': {
                    'TEXT': 'this key and subkeys',
                    'BITS': win32security.CONTAINER_INHERIT_ACE},
                'SUBKEYS': {
                    'TEXT': 'subkeys only',
                    'BITS': win32security.INHERIT_ONLY_ACE |
                    win32security.CONTAINER_INHERIT_ACE},
                'THIS KEY ONLY': {
                    'TEXT': 'this key only',
                    'BITS': win32security.NO_INHERITANCE},
                'THIS KEY AND SUBKEYS': {
                    'TEXT': 'this key and subkeys',
                    'BITS': win32security.CONTAINER_INHERIT_ACE},
                'SUBKEYS ONLY': {
                    'TEXT': 'subkeys only',
                    'BITS': win32security.INHERIT_ONLY_ACE |
                    win32security.CONTAINER_INHERIT_ACE}
            },
            win32security.SE_FILE_OBJECT: {
                'FILE': {
                    'TEXT': 'this file/folder only',
                    'BITS': win32security.NO_INHERITANCE},
                'FOLDER': {
                    'TEXT': 'this file/folder only',
                    'BITS': win32security.NO_INHERITANCE},
                'FOLDER&SUBFOLDERS&FILES': {
                    'TEXT': 'this folder, subfolders, and files',
                    'BITS': win32security.CONTAINER_INHERIT_ACE |
                    win32security.OBJECT_INHERIT_ACE},
                'FOLDER&SUBFOLDERS': {
                    'TEXT': 'this folder and subfolders',
                    'BITS': win32security.CONTAINER_INHERIT_ACE},
                'FOLDER&FILES': {
                    'TEXT': 'this folder and files',
                    'BITS': win32security.OBJECT_INHERIT_ACE},
                'SUBFOLDERS&FILES': {
                    'TEXT': 'subfolders and files',
                    'BITS': win32security.INHERIT_ONLY_ACE |
                    win32security.CONTAINER_INHERIT_ACE |
                    win32security.OBJECT_INHERIT_ACE},
                'SUBFOLDERS': {
                    'TEXT': 'subfolders only',
                    'BITS': win32security.INHERIT_ONLY_ACE |
                    win32security.CONTAINER_INHERIT_ACE},
                'FILES': {
                    'TEXT': 'files only',
                    'BITS': win32security.INHERIT_ONLY_ACE |
                    win32security.OBJECT_INHERIT_ACE},
                'THIS FILE ONLY': {
                    'TEXT': 'this file/folder only',
                    'BITS': win32security.NO_INHERITANCE},
                'THIS FOLDER ONLY': {
                    'TEXT': 'this file/folder only',
                    'BITS': win32security.NO_INHERITANCE},
                'THIS FOLDER, SUBFOLDERS, AND FILES': {
                    'TEXT': 'this folder, subfolders, and files',
                    'BITS': win32security.CONTAINER_INHERIT_ACE |
                    win32security.OBJECT_INHERIT_ACE},
                'THIS FOLDER AND SUBFOLDERS': {
                    'TEXT': 'this folder and subfolders',
                    'BITS': win32security.CONTAINER_INHERIT_ACE},
                'THIS FOLDER AND FILES': {
                    'TEXT': 'this folder and files',
                    'BITS': win32security.OBJECT_INHERIT_ACE},
                'SUBFOLDERS AND FILES': {
                    'TEXT': 'subfolders and files',
                    'BITS': win32security.INHERIT_ONLY_ACE |
                    win32security.CONTAINER_INHERIT_ACE |
                    win32security.OBJECT_INHERIT_ACE},
                'SUBFOLDERS ONLY': {
                    'TEXT': 'subfolders only',
                    'BITS': win32security.INHERIT_ONLY_ACE |
                    win32security.CONTAINER_INHERIT_ACE},
                'FILES ONLY': {
                    'TEXT': 'files only',
                    'BITS': win32security.INHERIT_ONLY_ACE |
                    win32security.OBJECT_INHERIT_ACE}
            }
        }

        self.objectType = {
            'FILE': win32security.SE_FILE_OBJECT,
            'DIRECTORY': win32security.SE_FILE_OBJECT,
            'REGISTRY': win32security.SE_REGISTRY_KEY}

    def getObjectTypeBit(self, t):
        '''
        returns the bit value of the string object type
        返回字符串对象类型的位值.
        '''
        if isinstance(t, str):
            t = t.upper()
            try:
                return self.objectType[t]
            except KeyError:
                print(123)
        else:
            return t

    def getSecurityHkey(self, s):
        '''
        returns the necessary string value for an HKEY for the win32security module
        返回的win32security模块HKEY必要的字符串值
        '''
        try:
            return self.hkeys_security[s]
        except KeyError:
            print(123)

    def getPermissionBit(self, t, m):
        '''
        returns a permission bit of the string permission value for the specified object type
        返回指定对象类型的字符串权限值的权限位.
        '''
        try:
            if isinstance(m, str):
                return self.rights[t][m]['BITS']
            else:
                return m
        except KeyError:
            print(123)

    def getPermissionText(self, t, m):
        '''
        returns the permission textual representation of a specified permission bit/object type
        '''
        try:
            return self.rights[t][m]['TEXT']
        except KeyError:
            print(123)

    def getAceTypeBit(self, t):
        '''
        returns the acetype bit of a text value
        '''
        try:
            return self.validAceTypes[t]['BITS']
        except KeyError:
            print(123)

    def getAceTypeText(self, t):
        '''
        returns the textual representation of a acetype bit
        '''
        try:
            return self.validAceTypes[t]['TEXT']
        except KeyError:
            print(123)

    def getPropagationBit(self, t, p):
        '''
        returns the propagation bit of a text value
        '''
        try:
            return self.validPropagations[t][p]['BITS']
        except KeyError:
            print(123)

    def getPropagationText(self, t, p):
        '''
        returns the textual representation of a propagation bit
        '''
        try:
            return self.validPropagations[t][p]['TEXT']
        except KeyError:
            print(123)

    def processPath(self, path, objectType):
        '''
        processes a path/object type combo and returns:
            registry types with the correct HKEY text representation
            files/directories with environment variables expanded
        '''
        if objectType == win32security.SE_REGISTRY_KEY:
            splt = path.split("\\")
            hive = self.getSecurityHkey(splt.pop(0).upper())
            splt.insert(0, hive)
            path = r'\\'.join(splt)
        else:
            path = os.path.expandvars(path)
        return path


def _getUserSid(user):
    '''
    return a state error dictionary, with 'sid' as a field if it could be returned
    if user is None, sid will also be None
    '''
    ret = {}

    sid_pattern = r'^S-1(-\d+){1,}$'

    if user and re.match(sid_pattern, user, re.I):
        try:
            sid = win32security.GetBinarySid(user)
        except Exception as e:
            ret['result'] = False
            ret['comment'] = 'Unable to obtain the binary security identifier for {0}.  The exception was {1}.'.format(
                user, e)
        else:
            try:
                win32security.LookupAccountSid('', sid)
                ret['result'] = True
                ret['sid'] = sid
            except Exception as e:
                ret['result'] = False
                ret['comment'] = 'Unable to lookup the account for the security identifier {0}.  The exception was {1}.'.format(
                    user, e)
    else:
        try:
            sid = win32security.LookupAccountName('', user)[0] if user else None
            ret['result'] = True
            ret['sid'] = sid
        except Exception as e:
            ret['result'] = False
            ret['comment'] = 'Unable to obtain the security identifier for {0}.  The exception was {1}.'.format(
                user, e)
    return ret





def _get_dacl(path, objectType):
    '''
    Gets the DACL of a path
    '''
    try:
        dacl = win32security.GetNamedSecurityInfo(
            path, objectType, win32security.DACL_SECURITY_INFORMATION
            ).GetSecurityDescriptorDacl()
    except Exception:
        dacl = None
    return dacl


def get(path, objectType, user=None):
    '''
    Get the ACL of an object. Will filter by user if one is provided.

    Args:
        path: The path to the object
        objectType: The type of object (FILE, DIRECTORY, REGISTRY)
        user: A user name to filter by

    Returns (dict): A dictionary containing the ACL

    CLI Example:

    .. code-block:: bash

        salt 'minion-id' win_dacl.get c:\temp directory
    '''
    ret = {'Path': path,
           'ACLs': []}

    sidRet = _getUserSid(user)

    if path and objectType:
        dc = daclConstants()
        objectTypeBit = dc.getObjectTypeBit(objectType)
        path = dc.processPath(path, objectTypeBit)
        tdacl = _get_dacl(path, objectTypeBit)
        if tdacl:
            for counter in range(0, tdacl.GetAceCount()):
                tAce = tdacl.GetAce(counter)
                if not sidRet['sid'] or (tAce[2] == sidRet['sid']):
                    ret['ACLs'].append(_ace_to_text(tAce, objectTypeBit))
    return ret


def add_ace(path, objectType, user, permission, acetype, propagation):
    r'''
    add an ace to an object

    path:  path to the object (i.e. c:\\temp\\file, HKEY_LOCAL_MACHINE\\SOFTWARE\\KEY, etc)
    user: user to add
    permission:  permissions for the user
    acetype:  either allow/deny for each user/permission (ALLOW, DENY)
    propagation: how the ACE applies to children for Registry Keys and Directories(KEY, KEY&SUBKEYS, SUBKEYS)

    CLI Example:

    .. code-block:: bash

        allow domain\fakeuser full control on HKLM\\SOFTWARE\\somekey, propagate to this key and subkeys
            salt 'myminion' win_dacl.add_ace 'HKEY_LOCAL_MACHINE\\SOFTWARE\\somekey' 'Registry' 'domain\fakeuser' 'FULLCONTROL' 'ALLOW' 'KEY&SUBKEYS'
    '''
    ret = {'result': None,
           'changes': {},
           'comment': ''}

    if (path and user and
            permission and acetype
            and propagation):
        if objectType.upper() == "FILE":
            propagation = "FILE"
        dc = daclConstants()
        objectTypeBit = dc.getObjectTypeBit(objectType)
        path = dc.processPath(path, objectTypeBit)
        user = user.strip()
        permission = permission.strip().upper()
        acetype = acetype.strip().upper()
        propagation = propagation.strip().upper()

        sidRet = _getUserSid(user)
        if not sidRet['result']:
            return sidRet
        permissionbit = dc.getPermissionBit(objectTypeBit, permission)
        acetypebit = dc.getAceTypeBit(acetype)
        propagationbit = dc.getPropagationBit(objectTypeBit, propagation)
        dacl = _get_dacl(path, objectTypeBit)

        if dacl:
            acesAdded = []
            try:
                if acetypebit == 0:
                    dacl.AddAccessAllowedAceEx(win32security.ACL_REVISION, propagationbit, permissionbit, sidRet['sid'])
                elif acetypebit == 1:
                    dacl.AddAccessDeniedAceEx(win32security.ACL_REVISION, propagationbit, permissionbit, sidRet['sid'])
                win32security.SetNamedSecurityInfo(
                    path, objectTypeBit, win32security.DACL_SECURITY_INFORMATION,
                    None, None, dacl, None)
                acesAdded.append((
                    '{0} {1} {2} on {3}'
                    ).format(
                    user, dc.getAceTypeText(acetype), dc.getPermissionText(objectTypeBit, permission),
                    dc.getPropagationText(objectTypeBit, propagation)))
                ret['result'] = True
            except Exception as e:
                ret['comment'] = 'An error occurred attempting to add the ace.  The error was {0}'.format(e)
                ret['result'] = False
                return ret
            if acesAdded:
                ret['changes']['Added ACEs'] = acesAdded
        else:
            ret['comment'] = 'Unable to obtain the DACL of {0}'.format(path)
    else:
        ret['comment'] = 'An empty value was specified for a required item.'
        ret['result'] = False
    return ret


def rm_ace(path, objectType, user, permission=None, acetype=None, propagation=None):
    r'''
    remove an ace to an object  删除一个王牌到一个对象

    path:  path to the object (i.e. c:\\temp\\file, HKEY_LOCAL_MACHINE\\SOFTWARE\\KEY, etc) 路径：路径的对象（即C：\温度\文件，hkey_local_machine \软件\键，等）
    user: user to remove 用户：用户删除
    permission:  permissions for the user 权限：用户的权限
    acetypes:  either allow/deny for each user/permission (ALLOW, DENY)   acetypes：要么允许/拒绝为每个用户/权限（允许，拒绝）
    propagation: how the ACE applies to children for Registry Keys and Directories(KEY, KEY&SUBKEYS, SUBKEYS)
    如何传播：ACE用于注册表和目录的孩子（重点，重点子项，子项）
    If any of the optional parameters are omitted (or set to None) they act as wildcards.
    如果任何可选的参数被省略（或设置为None）他们作为通配符
    CLI Example:
    CLI的例子：
    .. code-block:: bash
    删除允许域fakeuser完全控制在HKLM \软件\关键传播到这个键和子键
    盐的myminion”win_dacl.rm_ace '注册' hkey_local_machine \软件\关键的领域fakeuser '完全'允许'键和子键的
        remove allow domain\fakeuser full control on HKLM\\SOFTWARE\\somekey propagated to this key and subkeys
            salt 'myminion' win_dacl.rm_ace 'Registry' 'HKEY_LOCAL_MACHINE\\SOFTWARE\\somekey' 'domain\fakeuser' 'FULLCONTROL' 'ALLOW' 'KEY&SUBKEYS'
    '''
    ret = {'result': None,
           'changes': {},
           'comment': ''}

    if path and user:
        dc = daclConstants()
        if propagation and objectType.upper() == "FILE":
            propagation = "FILE"
        objectTypeBit = dc.getObjectTypeBit(objectType)
        path = dc.processPath(path, objectTypeBit)

        user = user.strip()
        permission = permission.strip().upper() if permission else None
        acetype = acetype.strip().upper() if acetype else None
        propagation = propagation.strip().upper() if propagation else None

        if check_ace(path, objectType, user, permission, acetype, propagation, True)['Exists']:
            sidRet = _getUserSid(user)
            if not sidRet['result']:
                return sidRet
            permissionbit = dc.getPermissionBit(objectTypeBit, permission) if permission else None
            acetypebit = dc.getAceTypeBit(acetype) if acetype else None
            propagationbit = dc.getPropagationBit(objectTypeBit, propagation) if propagation else None
            dacl = _get_dacl(path, objectTypeBit)
            counter = 0
            acesRemoved = []
            while counter < dacl.GetAceCount():
                tAce = dacl.GetAce(counter)
                if (tAce[0][1] & win32security.INHERITED_ACE) != win32security.INHERITED_ACE:
                    if tAce[2] == sidRet['sid']:
                        if not acetypebit or tAce[0][0] == acetypebit:
                            if not propagationbit or ((tAce[0][1] & propagationbit) == propagationbit):
                                if not permissionbit or tAce[1] == permissionbit:
                                    dacl.DeleteAce(counter)
                                    counter = counter - 1
                                    acesRemoved.append(_ace_to_text(tAce, objectTypeBit))

                counter = counter + 1
            if acesRemoved:
                try:
                    win32security.SetNamedSecurityInfo(
                        path, objectTypeBit, win32security.DACL_SECURITY_INFORMATION,
                        None, None, dacl, None)
                    ret['changes']['Removed ACEs'] = acesRemoved
                    ret['result'] = True
                except Exception as e:
                    ret['result'] = False
                    ret['comment'] = 'Error removing ACE.  The error was {0}.'.format(e)
                    return ret
        else:
            ret['comment'] = 'The specified ACE was not found on the path.'
    return ret


def _ace_to_text(ace, objectType):
    '''
    helper function to convert an ace to a textual representation
    '''
    dc = daclConstants()
    objectType = dc.getObjectTypeBit(objectType)
    try:
        userSid = win32security.LookupAccountSid('', ace[2])
        if userSid[1]:
            userSid = '{1}\\{0}'.format(userSid[0], userSid[1])
        else:
            userSid = '{0}'.format(userSid[0])
    except Exception:
        userSid = win32security.ConvertSidToStringSid(ace[2])
    tPerm = ace[1]
    tAceType = ace[0][0]
    tProps = ace[0][1]
    tInherited = ''
    for x in dc.validAceTypes:
        if dc.validAceTypes[x]['BITS'] == tAceType:
            tAceType = dc.validAceTypes[x]['TEXT']
            break
    for x in dc.rights[objectType]:
        if dc.rights[objectType][x]['BITS'] == tPerm:
            tPerm = dc.rights[objectType][x]['TEXT']
            break
    if (tProps & win32security.INHERITED_ACE) == win32security.INHERITED_ACE:
        tInherited = '[Inherited]'
        tProps = (tProps ^ win32security.INHERITED_ACE)
    for x in dc.validPropagations[objectType]:
        if dc.validPropagations[objectType][x]['BITS'] == tProps:
            tProps = dc.validPropagations[objectType][x]['TEXT']
            break
    return ((
        '{0} {1} {2} on {3} {4}'
        ).format(userSid, tAceType, tPerm, tProps, tInherited))


def _set_dacl_inheritance(path, objectType, inheritance=True, copy=True, clear=False):
    '''
    helper function to set the inheritance
    '''
    ret = {'result': False,
           'comment': '',
           'changes': {}}

    if path:
        try:
            sd = win32security.GetNamedSecurityInfo(path, objectType, win32security.DACL_SECURITY_INFORMATION)
            tdacl = sd.GetSecurityDescriptorDacl()
            if inheritance:
                if clear:
                    counter = 0
                    removedAces = []
                    while counter < tdacl.GetAceCount():
                        tAce = tdacl.GetAce(counter)
                        if (tAce[0][1] & win32security.INHERITED_ACE) != win32security.INHERITED_ACE:
                            tdacl.DeleteAce(counter)
                            removedAces.append(_ace_to_text(tAce, objectType))
                        else:
                            counter = counter + 1
                    if removedAces:
                        ret['changes']['Removed ACEs'] = removedAces
                else:
                    ret['changes']['Non-Inherited ACEs'] = 'Left in the DACL'
                win32security.SetNamedSecurityInfo(
                    path, objectType,
                    win32security.DACL_SECURITY_INFORMATION | win32security.UNPROTECTED_DACL_SECURITY_INFORMATION,
                    None, None, tdacl, None)
                ret['changes']['Inheritance'] = 'Enabled'
            else:
                if not copy:
                    counter = 0
                    inheritedAcesRemoved = []
                    while counter < tdacl.GetAceCount():
                        tAce = tdacl.GetAce(counter)
                        if (tAce[0][1] & win32security.INHERITED_ACE) == win32security.INHERITED_ACE:
                            tdacl.DeleteAce(counter)
                            inheritedAcesRemoved.append(_ace_to_text(tAce, objectType))
                        else:
                            counter = counter + 1
                    if inheritedAcesRemoved:
                        ret['changes']['Removed ACEs'] = inheritedAcesRemoved
                else:
                    ret['changes']['Previously Inherited ACEs'] = 'Copied to the DACL'
                win32security.SetNamedSecurityInfo(
                    path, objectType,
                    win32security.DACL_SECURITY_INFORMATION | win32security.PROTECTED_DACL_SECURITY_INFORMATION,
                    None, None, tdacl, None)
                ret['changes']['Inheritance'] = 'Disabled'
            ret['result'] = True
        except Exception as e:
            ret['result'] = False
            ret['comment'] = 'Error attempting to set the inheritance.  The error was {0}.'.format(e)

    return ret


def enable_inheritance(path, objectType, clear=False):
    '''
    enable/disable inheritance on an object

    Args:
        path: The path to the object
        objectType: The type of object (FILE, DIRECTORY, REGISTRY)
        clear: True will remove non-Inherited ACEs from the ACL

    Returns (dict): A dictionary containing the results

    CLI Example:

    .. code-block:: bash

        salt 'minion-id' win_dacl.enable_inheritance c:\temp directory
    '''
    dc = daclConstants()
    objectType = dc.getObjectTypeBit(objectType)
    path = dc.processPath(path, objectType)

    return _set_dacl_inheritance(path, objectType, True, None, clear)


def disable_inheritance(path, objectType, copy=True):
    '''
    Disable inheritance on an object
    禁用对象上的继承

    Args:
        path: The path to the object  路径：对象的路径
        objectType: The type of object (FILE, DIRECTORY, REGISTRY) 对象类型：对象的类型（文件、目录、注册表）
        copy: True will copy the Inherited ACEs to the DACL before disabling inheritance 复制：真的会复制继承的ACE的DACL之前禁用继承

    Returns (dict): A dictionary containing the results 返回（字典）：字典包含结果

    CLI Example:

    .. code-block:: bash

        salt 'minion-id' win_dacl.disable_inheritance c:\temp directory
    '''
    dc = daclConstants()
    objectType = dc.getObjectTypeBit(objectType)
    path = dc.processPath(path, objectType)

    return _set_dacl_inheritance(path, objectType, False, copy, None)


def check_inheritance(path, objectType, user=None):
    '''
    Check a specified path to verify if inheritance is enabled

    Args:
        path: path of the registry key or file system object to check
        objectType: The type of object (FILE, DIRECTORY, REGISTRY)
        user: if provided, will consider only the ACEs for that user

    Returns (bool): 'Inheritance' of True/False

    CLI Example:

    .. code-block:: bash

        salt 'minion-id' win_dacl.check_inheritance c:\temp directory <username>
    '''

    ret = {'result': False,
           'Inheritance': False,
           'comment': ''}

    sidRet = _getUserSid(user)

    dc = daclConstants()
    objectType = dc.getObjectTypeBit(objectType)
    path = dc.processPath(path, objectType)

    try:
        sd = win32security.GetNamedSecurityInfo(path, objectType, win32security.DACL_SECURITY_INFORMATION)
        dacls = sd.GetSecurityDescriptorDacl()
    except Exception as e:
        ret['result'] = False
        ret['comment'] = 'Error obtaining the Security Descriptor or DACL of the path: {0}.'.format(e)
        return ret

    for counter in range(0, dacls.GetAceCount()):
        ace = dacls.GetAce(counter)
        if (ace[0][1] & win32security.INHERITED_ACE) == win32security.INHERITED_ACE:
            if not sidRet['sid'] or ace[2] == sidRet['sid']:
                ret['Inheritance'] = True
                break

    ret['result'] = True
    return ret


def check_ace(path, objectType, user, permission=None, acetype=None, propagation=None, exactPermissionMatch=False):
    '''
    Checks a path to verify the ACE (access control entry) specified exists

    Args:
        path:  path to the file/reg key
        objectType: The type of object (FILE, DIRECTORY, REGISTRY)
        user:  user that the ACL is for
        permission:  permission to test for (READ, FULLCONTROL, etc)
        acetype:  the type of ACE (ALLOW or DENY)
        propagation:  the propagation type of the ACE (FILES, FOLDERS, KEY, KEY&SUBKEYS, SUBKEYS, etc)
        exactPermissionMatch:  the ACL must match exactly, IE if READ is specified, the user must have READ exactly and not FULLCONTROL (which also has the READ permission obviously)

    Returns (dict): 'Exists' true if the ACE exists, false if it does not

    CLI Example:

    .. code-block:: bash

        salt 'minion-id' win_dacl.check_ace c:\temp directory <username> fullcontrol
    '''
    ret = {'result': False,
           'Exists': False,
           'comment': ''}

    dc = daclConstants()
    objectTypeBit = dc.getObjectTypeBit(objectType)
    path = dc.processPath(path, objectTypeBit)

    permission = permission.upper() if permission else None
    acetype = acetype.upper() if permission else None
    propagation = propagation.upper() if propagation else None

    permissionbit = dc.getPermissionBit(objectTypeBit, permission) if permission else None
    acetypebit = dc.getAceTypeBit(acetype) if acetype else None
    propagationbit = dc.getPropagationBit(objectTypeBit, propagation) if propagation else None

    sidRet = _getUserSid(user)
    if not sidRet['result']:
        return sidRet

    dacls = _get_dacl(path, objectTypeBit)
    ret['result'] = True
    if dacls:
        for counter in range(0, dacls.GetAceCount()):
            ace = dacls.GetAce(counter)
            if ace[2] == sidRet['sid']:
                if not acetypebit or ace[0][0] == acetypebit:
                    if not propagationbit or (ace[0][1] & propagationbit) == propagationbit:
                        if not permissionbit:
                            ret['Exists'] = True
                            return ret
                        if exactPermissionMatch:
                            if ace[1] == permissionbit:
                                ret['Exists'] = True
                                return ret
                        else:
                            if (ace[1] & permissionbit) == permissionbit:
                                ret['Exists'] = True
                                return ret
    else:
        ret['comment'] = 'No DACL found for object.'
    return ret