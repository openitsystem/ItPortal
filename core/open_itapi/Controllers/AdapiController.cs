using System;
using System.Net.Http;
using System.Web.Http;
using System.Web.Security;
using System.Web.Configuration;
using System.Text;
using System.DirectoryServices;
using System.Web.Script.Serialization;
using System.Security.Principal;
using System.Security.AccessControl;
using System.Collections.Generic;
using ActiveDs;
using System.Security;
using System.Management.Automation;
using System.Management.Automation.Runspaces;
using System.Threading;
using System.Collections;
using System.Runtime.InteropServices;
using Mysqlapi.Controllers;
using System.Configuration;
using System.Security.Cryptography;
using System.Linq;
using System.DirectoryServices.ActiveDirectory;
using System.Net;

namespace open_itapi.Controllers
{
    public class AdapiController : ApiController
    {
        #region 标志参数
        public enum ADS_USER_FLAG_ENUM
        {
            ///
            ///登录脚本标志。如果通过 ADSI LDAP 进行读或写操作时，该标志失效。如果通过 ADSI WINNT，该标志为只读。
            ///
            ADS_UF_SCRIPT = 0X0001,
            ///
            ///用户帐号禁用标志
            ///
            ADS_UF_ACCOUNTDISABLE = 0X0002,
            ///
            ///主文件夹标志
            ///
            ADS_UF_HOMEDIR_REQUIRED = 0X0008,
            ///
            ///过期标志
            ///
            ADS_UF_LOCKOUT = 0X0010,
            ///
            ///用户密码不是必须的
            ///
            ADS_UF_PASSWD_NOTREQD = 0X0020,
            ///
            ///密码不能更改标志
            ///
            ADS_UF_PASSWD_CANT_CHANGE = 0X0040,
            ///
            ///使用可逆的加密保存密码
            ///
            ADS_UF_ENCRYPTED_TEXT_PASSWORD_ALLOWED = 0X0080,
            ///
            ///本地帐号标志
            ///
            ADS_UF_TEMP_DUPLICATE_ACCOUNT = 0X0100,
            ///
            ///普通用户的默认帐号类型
            ///
            ADS_UF_NORMAL_ACCOUNT = 0X0200,
            ///
            ///跨域的信任帐号标志
            ///
            ADS_UF_INTERDOMAIN_TRUST_ACCOUNT = 0X0800,
            ///
            ///工作站信任帐号标志
            ///
            ADS_UF_WORKSTATION_TRUST_ACCOUNT = 0x1000,
            ///
            ///服务器信任帐号标志
            ///
            ADS_UF_SERVER_TRUST_ACCOUNT = 0X2000,
            ///
            ///密码永不过期标志
            ///
            ADS_UF_DONT_EXPIRE_PASSWD = 0X10000,
            ///
            /// MNS 帐号标志
            ///
            ADS_UF_MNS_LOGON_ACCOUNT = 0X20000,
            ///
            ///交互式登录必须使用智能卡
            ///
            ADS_UF_SMARTCARD_REQUIRED = 0X40000,
            ///
            ///当设置该标志时，服务帐号（用户或计算机帐号）将通过 Kerberos 委托信任
            ///
            ADS_UF_TRUSTED_FOR_DELEGATION = 0X80000,
            ///
            ///当设置该标志时，即使服务帐号是通过 Kerberos 委托信任的，敏感帐号不能被委托
            ///
            ADS_UF_NOT_DELEGATED = 0X100000,
            ///
            ///此帐号需要 DES 加密类型
            ///
            ADS_UF_USE_DES_KEY_ONLY = 0X200000,
            ///
            ///不要进行 Kerberos 预身份验证
            ///
            ADS_UF_DONT_REQUIRE_PREAUTH = 0X4000000,
            ///
            ///用户密码过期标志
            ///
            ADS_UF_PASSWORD_EXPIRED = 0X800000,
            ///
            ///用户帐号可委托标志
            ///
            ADS_UF_TRUSTED_TO_AUTHENTICATE_FOR_DELEGATION = 0X1000000
        }

        private static int userlockvalue;
        public enum GroupType : uint
        {
            GLOBAL = 0x2,
            DOMAIN_LOCAL = 0x4,
            UNIVERSAL = 0x8,
            SECURITY = 0x80000000
        }
        #endregion


        #region MD5
        public static string admd5(string domain)
        {
            try
            {
                Mysqldbinfo dbinfo = new Mysqldbinfo();
                Dictionary<string, string> sel = dbinfo.Selglobalsnocolumn(domain);
                string result = sel["skey"];
                return result;
            }
            catch (Exception)
            {
                return "ghdfgherwert^&#^(*$&GAJGSHF&*@!(&HRGHGDKBFAHGSYQWG";
            }
        }

        public static string admd5_nodomain()
        {
            try
            {
                Mysqldbinfo dbinfo = new Mysqldbinfo();
                Dictionary<string, string> sel = dbinfo.Selglobals_noDecrypction();
                string result = sel["skey"];
                return result;
            }
            catch (Exception)
            {
                return "ghdfgherwert^&#^(*$&GAJGSHF&*@!(&HRGHGDKBFAHGSYQWG";
            }
        }

        #endregion

        #region 把数据格式转换成Json
        /// <summary>
        /// 把数据格式转换成Json
        /// </summary>
        /// <param name="obj"></param>
        /// <returns></returns>
        public static HttpResponseMessage toJson(Object obj)
        {
            String str;
            if (obj is String || obj is Char)
            {
                str = obj.ToString();
            }
            else
            {
                JavaScriptSerializer serializer = new JavaScriptSerializer();
                serializer.MaxJsonLength = Int32.MaxValue;
                str = serializer.Serialize(obj);

            }
            HttpResponseMessage result = new HttpResponseMessage { Content = new StringContent(str, Encoding.GetEncoding("UTF-8"), "application/json") };
            return result;
        }
        #endregion
        #region 大整数属性类型和时间类型的相互转换 
        /// <summary>
        /// 从 IADsLargeInteger 类型转换为 DateTime 类型。
        /// </summary>
        /// <param name="largeIntValue"></param>
        /// <returns></returns>
        public static DateTime GetDateTimeFromLargeInteger(IADsLargeInteger largeIntValue)
        {
            //
            // Convert large integer to int64 value
            //将大整数转换为int64值
            long int64Value = (long)((uint)largeIntValue.LowPart +
                     (((long)largeIntValue.HighPart) << 32));

            //
            // Return the DateTime in utc
            //将大整数转换为int64值
            return DateTime.FromFileTimeUtc(int64Value);
        }
        /// <summary>
        /// 从 DateTime 格式转换为 IADsLargeInteger。
        /// </summary>
        /// <param name="dateTimeValue"></param>
        /// <returns></returns>
        public static IADsLargeInteger GetLargeIntegerFromDateTime(DateTime dateTimeValue)
        {
            //
            // Convert DateTime value to utc file time
            //Convert DateTime value to utc file time
            Int64 int64Value = dateTimeValue.ToFileTimeUtc();

            //
            // convert to large integer
            //转换成大整数
            IADsLargeInteger largeIntValue = (IADsLargeInteger)new LargeInteger();

            largeIntValue.HighPart = (int)(int64Value >> 32);
            largeIntValue.LowPart = (int)(int64Value & 0xFFFFFFFF);

            return largeIntValue;
        }
        #endregion

        /// <summary>
        /// 获取powershell登陆状态
        /// </summary>
        /// <returns></returns>
        public WSManConnectionInfo mailexloginin(string domain)
        {
            Mysqldbinfo dbinfo = new Mysqldbinfo();
            Dictionary<string, string> sel = dbinfo.Selglobals(domain);
            SecureString ssRunasPassword = new SecureString();
            foreach (char x in sel["ex_password"])
            {
                ssRunasPassword.AppendChar(x);
            }
            PSCredential credentials = new PSCredential(sel["ex_domain"] +"\\"+ sel["ex_account"], ssRunasPassword);
            //var connInfo = new WSManConnectionInfo(new Uri("http://0.0.0.0/PowerShell"), "http://schemas.microsoft.com/powershell/Microsoft.Exchange", credentials);
            var connInfo = new WSManConnectionInfo(new Uri("http://"+ sel["ex_ip"] + "/PowerShell"), "http://schemas.microsoft.com/powershell/Microsoft.Exchange", credentials);
            connInfo.AuthenticationMechanism = AuthenticationMechanism.Basic;
            return connInfo;
        }

        /// <summary>
        /// 解密
        /// </summary>
        /// <returns></returns>
        public string Decrypction(string toDecrypt)
        {
            try { 
            string key = "@0yKGh%AGzwG0P*dXxj9!3ed2RSXz11E";
            string iv = "OZ3sfNy7HxIkx5Vk";
            byte[] keyArray = UTF8Encoding.UTF8.GetBytes(key);
            byte[] ivArray = UTF8Encoding.UTF8.GetBytes(iv);
            byte[] toEncryptArray = Convert.FromBase64String(toDecrypt);
            RijndaelManaged rDel = new RijndaelManaged();
            rDel.Key = keyArray;
            rDel.IV = ivArray;
            rDel.Mode = CipherMode.ECB;
            rDel.Padding = PaddingMode.Zeros;
            ICryptoTransform cTransform = rDel.CreateDecryptor();
            byte[] resultArray = cTransform.TransformFinalBlock(toEncryptArray, 0, toEncryptArray.Length);
            return (UTF8Encoding.UTF8.GetString(resultArray)).Replace("\u0000", "");

        }
            catch (Exception)
            {
                return "False";
            }
        }

        #region 传入OU路径（格式：/  从大到小，中间加/)转 
        /// <summary>
        /// 获得OU的Path
        /// </summary>
        /// <param name="organizeUnit">OU名</param>
        /// <returns></returns>
        public static string GetOrganizeNamePath(string organizeUnit, string domain)
        {
            Mysqldbinfo dbinfo = new Mysqldbinfo();
            Dictionary<string, string> sel = dbinfo.Selglobals(domain);
            StringBuilder sb = new StringBuilder();
            sb.Append(sel["_ldapIdentity"]);
            return sb.Append(SplitOrganizeNameToDN(organizeUnit, domain)).ToString();
        }
        /// <summary>
        /// </summary>
        /// <param name="organizeName">组织名称</param>
        /// <returns>返回一个级别</returns>
        public static string SplitOrganizeNameToDN(string organizeName, string domain)
        {
            Mysqldbinfo dbinfo = new Mysqldbinfo();
            Dictionary<string, string> sel = dbinfo.Selglobals(domain);
            StringBuilder sb = new StringBuilder();

            if (organizeName != null && organizeName.Length > 0)
            {
                string[] allOu = organizeName.Split(new char[] { '/', '\\' });
                for (int i = allOu.Length - 1; i >= 0; i--)
                {
                    string ou = allOu[i];
                    if (sb.Length > 0)
                    {
                        sb.Append(",");
                    }
                    sb.Append("OU=").Append(ou);
                }
            }

            //如果传入了组织名称，则添加,
            if (sb.Length > 0)
            {
                sb.Append(",");
            }
            sb.Append(sel["ad_path"]);
            return sb.ToString();
        }
        #endregion

        #region GetDirectoryObject  获得相应DirectoryEntry实体
        /// <summary>
        /// 获得相应DirectoryEntry实体
        /// </summary>
        /// <returns></returns>
        public static DirectoryEntry GetDirectoryObject(string domain)
        {
            Mysqldbinfo dbinfo = new Mysqldbinfo();
            Dictionary<string, string> sel = dbinfo.Selglobals(domain);
            DirectoryEntry entry = new DirectoryEntry(sel["_ldapIdentity"] + sel["ad_path"], sel["ad_domain"] + "\\" + sel["ad_account"], sel["ad_password"], AuthenticationTypes.Secure);
            return entry;
        }
        /// <summary>
        /// distinguishedName 传入，获取实体
        /// </summary>
        /// <param name="ouname"> </param>
        /// <returns></returns>
        public static DirectoryEntry GetDirectoryObjectforOU(string ouname, string domain)
        {
            Mysqldbinfo dbinfo = new Mysqldbinfo();
            Dictionary<string, string> sel = dbinfo.Selglobals(domain);
            DirectoryEntry entry = new DirectoryEntry(sel["_ldapIdentity"] + ouname, sel["ad_domain"] + "\\" + sel["ad_account"], sel["ad_password"], AuthenticationTypes.Secure);
            return entry;
        }
        /// <summary>
        /// 传入OU带，获取实体
        /// </summary>
        /// <param name="ouname"></param>
        /// <returns></returns>
        public static DirectoryEntry GetDirectoryObjectbyOU(string ouname, string domain)
        {
            Mysqldbinfo dbinfo = new Mysqldbinfo();
            Dictionary<string, string> sel = dbinfo.Selglobals(domain);

            DirectoryEntry entry = new DirectoryEntry(sel["_ldapIdentity"] + ouname + sel["ad_path"], sel["ad_domain"] + "\\" + sel["ad_account"], sel["ad_password"], AuthenticationTypes.Secure);
            return entry;
        }
        /// <summary>
        /// 根据IP获取当前IP的全局实体
        /// </summary>
        /// <param name="domainIpsg"></param>
        /// <returns></returns>
        public static DirectoryEntry GetDirectoryObjectIp(string domainIpsg, string domain)
        {
            Mysqldbinfo dbinfo = new Mysqldbinfo();
            Dictionary<string, string> sel = dbinfo.Selglobals(domain);
            DirectoryEntry entry = new DirectoryEntry("LDAP://" + domainIpsg + "/" + sel["ad_path"], sel["ad_domain"] + "\\" + sel["ad_account"], sel["ad_password"], AuthenticationTypes.Secure);
            return entry;
        }
        /// <summary>
        /// i.e.  方法重载
        /// 传入OU路径（格式：IT/  从大到小，中间加/)转 
        /// </summary>
        /// <param name="domainReference"></param>
        /// <returns></returns>
        public static DirectoryEntry GetDirectoryobject(string domainReference, string domain)
        {
            Mysqldbinfo dbinfo = new Mysqldbinfo();
            Dictionary<string, string> sel = dbinfo.Selglobals(domain);
            DirectoryEntry entry = new DirectoryEntry(GetOrganizeNamePath(domainReference, domain), sel["ad_domain"] + "\\" + sel["ad_account"], sel["ad_password"], AuthenticationTypes.Secure);
            return entry;
        }
        /// <summary>
        ///根据用户帐号称取得用户的对象
        ///用户帐号名
        ///如果找到该用户，则返回用户的对象；否则返回null
        /// </summary>
        /// <param name="sAMAccountName"></param>
        /// <returns></returns>
        public static DirectoryEntry GetDirectoryEntryByAccount(string sAMAccountName, string domain)
        {
            DirectoryEntry de = GetDirectoryObject(domain);
            DirectorySearcher deSearch = new DirectorySearcher(de);
            deSearch.Filter = "(&(&(objectCategory=person)(objectClass=user))(sAMAccountName=" + sAMAccountName + "))";
            deSearch.SearchScope = SearchScope.Subtree;
            try
            {
                SearchResult result = deSearch.FindOne();
                de = new DirectoryEntry(result.Path);
            }
            catch
            {
                de = null;
            }
            de.Close();
            return de;
        }

        /// <summary>
        ///根据用户工号称取得用户的对象
        ///用户帐号名
        ///如果找到该用户，则返回用户的对象；否则返回null
        /// </summary>
        /// <param name="jobnumber"></param>
        /// <returns></returns>
        public static SearchResult GetDirectoryEntryByJobnumber(string jobnumber, string domain)
        {
            DirectoryEntry de = GetDirectoryObject(domain);
            DirectorySearcher deSearch = new DirectorySearcher(de);
            deSearch.Filter = "(&(&(objectCategory=person)(objectClass=user))(wWWHomePage=" + jobnumber + "))";
            deSearch.SearchScope = SearchScope.Subtree;
            SearchResult result = deSearch.FindOne();
            de.Close();
            return result;
        }

        /// <summary>
        ///根据用户Gid称取得用户的对象
        ///用户帐号名
        ///如果找到该用户，则返回用户的对象；否则返回null
        /// </summary>
        /// <param name="jobnumber"></param>
        /// <returns></returns>
        public static SearchResult GetDirectoryEntryByGid(string guid, string domain)
        {
            DirectoryEntry de = GetDirectoryObject(domain);
            DirectorySearcher deSearch = new DirectorySearcher(de);
            deSearch.Filter = "(&(&(objectCategory=person)(objectClass=user))(physicalDeliveryOfficeName=" + guid + "))";
            deSearch.SearchScope = SearchScope.Subtree;
            SearchResult result = deSearch.FindOne();
            de.Close();
            return result;
        }

        public static SearchResult GetDirectoryEntryByDis(string displayName, string domain)
        {
            DirectoryEntry de = GetDirectoryObject(domain);
            DirectorySearcher deSearch = new DirectorySearcher(de);
            deSearch.Filter = "(&(&(objectCategory=person)(objectClass=user))(displayName=" + displayName + "))";
            deSearch.SearchScope = SearchScope.Subtree;
            SearchResult result = deSearch.FindOne();
            de.Close();
            return result;
        }

        /// <summary>
        ///根据用户smtp获取用户对象
        ///组名
        /// </summary>
        /// <param name="userName"></param>
        /// <returns></returns>
        public static SearchResult GetDirectoryEntryOfUserBySmtp(string userName, string domain)
        {
            DirectoryEntry de = GetDirectoryObject(domain);
            DirectorySearcher deSearch = new DirectorySearcher(de);
            deSearch.Filter = "(&(objectCategory=person)(objectClass=user) (proxyAddresses=smtp:" + userName + "))";
            deSearch.SearchScope = SearchScope.Subtree;
            SearchResult result = deSearch.FindOne();
            de.Close();
            return result;
        }


        /// <summary>
        ///根据用户名获取用户对象
        ///组名
        /// </summary>
        /// <param name="userName"></param>
        /// <returns></returns>
        public static SearchResult GetDirectoryEntryOfUser(string userName, string domain)
        {
            DirectoryEntry de = GetDirectoryObject(domain);
            DirectorySearcher deSearch = new DirectorySearcher(de);
            deSearch.Filter = "(&(objectCategory=person)(objectClass=user) (sAMAccountName=" + userName + "))";
            deSearch.SearchScope = SearchScope.Subtree;
            SearchResult result = deSearch.FindOne();
            de.Close();
            return result;
        }

        /// <summary>
        ///根据用户名,和制定服务器IP获取用户对象
        ///组名
        /// </summary>
        /// <param name="userName"></param>
        /// <param name="ip"></param>
        /// <returns></returns>
        public static SearchResult GetDirectoryEntryOfUser(string userName, string ip, string domain)
        {
            DirectoryEntry de = GetDirectoryObjectIp(ip, domain);
            DirectorySearcher deSearch = new DirectorySearcher(de);
            deSearch.Filter = "(&(objectCategory=person)(objectClass=user) (sAMAccountName=" + userName + "))";
            deSearch.SearchScope = SearchScope.Subtree;
            SearchResult result = deSearch.FindOne();
            de.Close();
            return result;
        }

        /// <summary>
        ///根据组名取得用户组的对象
        ///组名
        /// </summary>
        /// <param name="groupName"></param>
        /// <returns></returns>
        public static SearchResult GetDirectoryEntryOfGroup(string groupName, string domain)
        {
            DirectoryEntry de = GetDirectoryObject(domain);
            DirectorySearcher deSearch = new DirectorySearcher(de);
            deSearch.Filter = "(&(objectClass=group) (sAMAccountName=" + groupName + "))";
            deSearch.SearchScope = SearchScope.Subtree;
            SearchResult result = deSearch.FindOne();
            de.Close();
            return result;
        }
        /// <summary>
        /// 根据managedBy取得用户组的对象
        /// </summary>
        /// <param name="managedBy"></param>
        /// <param name="domain"></param>
        /// <returns></returns>
        public static SearchResultCollection GetDirectoryEntryOfmanagedBy(string managedBy, string domain)
        {
            DirectoryEntry de = GetDirectoryObject(domain);
            DirectorySearcher deSearch = new DirectorySearcher(de);
            deSearch.Filter = "(&(objectClass=group) (managedBy=" + managedBy + ")(mail=*))";
            deSearch.SearchScope = SearchScope.Subtree;
            SearchResultCollection result = deSearch.FindAll();
            de.Close();
            return result;
        }



        /// <summary>
        ///根据OU名取得OU的对象
        ///OU名
        /// </summary>
        /// <param name="groupName"></param>
        /// <returns></returns>
        public static SearchResult GetDirectoryEntryOfOu(string ouName, string domain)
        {
            DirectoryEntry de = GetDirectoryObject(domain);
            DirectorySearcher deSearch = new DirectorySearcher(de);
            deSearch.Filter = "(&(objectClass=OrganizationalUnit) (OU=" + ouName + "))";
            deSearch.SearchScope = SearchScope.Subtree;
            SearchResult result = deSearch.FindOne();
            de.Close();
            return result;
        }

        /// <summary>
        ///根据计算机名取得计算机的对象 修改
        ///OU名
        /// </summary>
        /// <param name="computername"></param>
        /// <returns></returns>
        public static SearchResult GetDirectoryEntryOfComputer(string computername, string domain)
        {
            DirectoryEntry de = GetDirectoryObject(domain);
            DirectorySearcher deSearch = new DirectorySearcher(de);
            deSearch.Filter = "(&(objectClass=Computer) (cn=" + computername + "))";
            deSearch.SearchScope = SearchScope.Subtree;
            SearchResult result = deSearch.FindOne();
            de.Close();
            return result;
        }
        /// <summary>
        /// 判断AD用户账号密码是否正确
        /// </summary>
        /// <param name="userName"></param>
        /// <param name="userPwd"></param>
        /// <param name="domain"></param>
        /// <returns></returns>
        public static bool VerifyUserLogin(string userName, string userPwd, string domain)
        {
            try
            {
                Mysqldbinfo dbinfo = new Mysqldbinfo();
                Dictionary<string, string> sel = dbinfo.Selglobals(domain);
                if (userPwd == null)
                {
                    return false;
                }
                // strADRootPath为该组织单元路径
                DirectoryEntry entry = new DirectoryEntry(sel["_ldapIdentity"] + sel["ad_path"], userName, userPwd);
                DirectorySearcher search = new DirectorySearcher(entry);
                SearchResult sr = search.FindOne();
                return true;
            }
            catch
            {
                return false;
            }
        }
        #endregion

        #region (1)判断是否存在  ObjectExists  
        /// <summary>
        /// 判断是否存在 user
        /// </summary>
        /// <param name="objectName"></param>
        /// <param name="catalog"></param>
        /// <returns></returns>
        [HttpGet]
        public bool ObjectExists(string objectName, string catalog, string domain)
        {
            if (objectName == null)
            {
                return false;
            }
            else
            {
                DirectoryEntry de = GetDirectoryObject(domain);
                DirectorySearcher deSearch = new DirectorySearcher();
                deSearch.SearchRoot = de;
                switch (catalog)
                {
                    case "user": deSearch.Filter = "(&(objectClass=user)(objectCategory=person) (sAMAccountName=" + objectName + "))"; break;
                    case "group": deSearch.Filter = "(&(objectClass=group) (cn=" + objectName + "))"; break;
                    case "organizationalUnit": deSearch.Filter = "(&(objectClass=organizationalUnit) (OU=" + objectName + "))"; break;
                    case "computer": deSearch.Filter = "(&(objectClass=computer) (cn=" + objectName + "))"; break;// 判断计算机是否存在
                    case "msExchDynamicDistributionList": deSearch.Filter = "(&(objectClass=msExchDynamicDistributionList) (cn=" + objectName + "))"; break;
                    default: break;
                }
                SearchResultCollection results = deSearch.FindAll();
                de.Close();
                if (results.Count == 0)
                {
                    return false;
                }
                else
                {
                    return true;
                }
            }
        }

        /// <summary>
        /// (1)判断是否存在AD  ObjectExistAD  
        /// </summary>
        /// <param name="objectName"></param>
        /// <returns></returns>
        [HttpGet]
        public bool ObjectExistAD(string objectName, string domain)
        {
            if (objectName == null)
            {
                return false;
            }
            else
            {
                Mysqldbinfo dbinfo = new Mysqldbinfo();
                Dictionary<string, string> sel = dbinfo.Selglobals(domain);
                DirectoryEntry de = GetDirectoryObject(domain);
                DirectorySearcher deSearch = new DirectorySearcher();
                deSearch.SearchRoot = de;
                deSearch.Filter = "(|(&(objectClass=user)(objectCategory=person) (|(sAMAccountName=" + objectName + ")(cn=" + objectName + ")(proxyAddresses=smtp:" + objectName + sel["fulldomain"] + ")))(&(objectClass=group) (cn=" + objectName + ")))";
                SearchResultCollection results = deSearch.FindAll();
                de.Close();
                if (results.Count == 0)
                {
                    return false;
                }
                else
                {
                    return true;
                }
            }
        }

        [HttpGet]
        public bool ObjectExistsOU(string objectName, string catalog, string ouname, string domain)
        {
            if (objectName == null)
            {
                return false;
            }
            else
            {
                DirectoryEntry de = GetDirectoryObjectforOU(ouname, domain);
                DirectorySearcher deSearch = new DirectorySearcher();
                deSearch.SearchRoot = de;
                switch (catalog)
                {
                    case "user": deSearch.Filter = "(&(objectClass=user)(objectCategory=person) (sAMAccountName=" + objectName + "))"; break;
                    case "group": deSearch.Filter = "(&(objectClass=group) (cn=" + objectName + "))"; break;
                    case "organizationalUnit": deSearch.SearchScope = SearchScope.OneLevel; deSearch.Filter = "(&(objectClass=organizationalUnit) (OU=" + objectName + "))"; break;
                    case "organizationalUnitSubtree": deSearch.Filter = "(&(objectClass=organizationalUnit) (OU=" + objectName + "))"; break;
                    case "computer": deSearch.Filter = "(&(objectClass=computer) (cn=" + objectName + "))"; break;
                    case "msExchDynamicDistributionList": deSearch.Filter = "(&(objectClass=msExchDynamicDistributionList) (cn=" + objectName + "))"; break;
                    default: break;
                }
                SearchResultCollection results = deSearch.FindAll();
                de.Close();
                if (results.Count == 0)
                {
                    return false;
                }
                else
                {
                    return true;
                }
            }
        }




        /// <summary>
        /// 根据类型和ou判断是否存在（单层OU）
        /// </summary>
        /// <param name="objectName"></param>
        /// <param name="catalog"></param>
        /// <param name="ouname"></param>
        /// <param name="domain"></param>
        /// <returns></returns>
        [HttpGet]
        public bool ObjectExistsOneOU(string objectName, string catalog, string ouname, string domain)
        {
            if (objectName == null)
            {
                return false;
            }
            else
            {
                DirectoryEntry de = GetDirectoryObjectforOU(ouname, domain);
                DirectorySearcher deSearch = new DirectorySearcher(de);
                deSearch.SearchScope = SearchScope.OneLevel;
                switch (catalog)
                {
                    case "user": deSearch.Filter = "(&(objectClass=user)(objectCategory=person) (sAMAccountName=" + objectName + "))"; break;
                    case "group": deSearch.Filter = "(&(objectClass=group) (cn=" + objectName + "))"; break;
                    case "organizationalUnit": deSearch.SearchScope = SearchScope.OneLevel; deSearch.Filter = "(&(objectClass=organizationalUnit) (OU=" + objectName + "))"; break;
                    case "organizationalUnitSubtree": deSearch.Filter = "(&(objectClass=organizationalUnit) (OU=" + objectName + "))"; break;
                    case "computer": deSearch.Filter = "(&(objectClass=computer) (cn=" + objectName + "))"; break;
                    case "msExchDynamicDistributionList": deSearch.Filter = "(&(objectClass=msExchDynamicDistributionList) (cn=" + objectName + "))"; break;
                    default: break;
                }
                SearchResultCollection results = deSearch.FindAll();
                de.Close();
                if (results.Count == 0)
                {
                    return false;
                }
                else
                {
                    return true;
                }
            }
        }
        #endregion

        #region (2)根据对象类别新建对象
        [HttpGet]
        public HttpResponseMessage Createobject(string objects, string oudn, string objectClass, string skey, string domain, string sn = null, string displayName = null, string wWWHomePage = null, string password = null, string guid = null)
        {
            var isSuccess = false;
            var message = new { message = "参数不能为空。" };
            if (skey == admd5(domain))
            {
                try
                {
                    switch (objectClass)
                    {
                        case "user":
                            {
                                Mysqldbinfo dbinfo = new Mysqldbinfo();
                                Dictionary<string, string> sel = dbinfo.Selglobals(domain);
                                DirectoryEntry de = GetDirectoryObjectforOU(oudn, domain);
                                DirectoryEntries users = de.Children;
                                DirectoryEntry newuser = users.Add("CN=" + objects, "user");//创建\
                                //常项选项卡
                                newuser.Properties["sn"].Value = sn;  //	姓(L)
                                newuser.Properties["givenName"].Value = sn;  //	名(F)
                                newuser.Properties["displayName"].Value = displayName; //显示名称S
                                newuser.Properties["description"].Value = sn;  //描述(D)  
                                newuser.Properties["wWWHomePage"].Value = wWWHomePage; //网页(W)

                                //newuser.Properties["initials"].Value = initials;  //	英文缩写(I)
                                newuser.Properties["physicalDeliveryOfficeName"].Value = guid;//办公室(C)                                                                       
                                //newuser.Properties["telephoneNumber"].Value = telephoneNumber; //电话号码(T)
                                //newuser.Properties["otherTelephone"].Value = otherTelephone; //电话号码-其它(O)...
                                //newuser.Properties["url"].Value = url; // 网页 - 其它(R)...
                                //帐户选项卡
                                newuser.Properties["sAMAccountName"].Value = objects; //用户登录名(Windows 2000 以前版本)(W)
                                newuser.Properties["userPrincipalName"].Value = objects + sel["fulldomain"];//用户登录名(U) 后面加当前                                                       
                                //组织选项卡
                                //newuser.Properties["company"].Value = company; //公司(C)  
                                //newuser.Properties["departmen"].Value = departmen; //部门(D)   
                                //newuser.Properties["title"].Value = title; //职务(J)    
                                //newuser.Properties["manager"].Value = manager; //经理-姓名(N)
                                //newuser.Properties["directReports"].Value = directReports; //直接下属(E)
                                newuser.CommitChanges();
                                newuser.Invoke("SetPassword", password);//设置密码 
                                //默认设置新增账户启用
                                newuser.Properties["userAccountControl"].Value = 0x200;//启用
                                newuser.CommitChanges();
                                newuser.Close();
                                de.Close();
                                isSuccess = true;
                                message = new
                                {
                                    message = objects + "添加成功",
                                };
                            }; break;

                        case "group":
                            {
                                if ((objects == string.Empty) || (oudn == string.Empty))
                                {
                                    message = new { message = objects + "参数不能为空。" };
                                }
                                else
                                {
                                    DirectoryEntry de = GetDirectoryObjectforOU(oudn, domain);
                                    DirectoryEntries Groups = de.Children;
                                    DirectoryEntry newgroup = Groups.Add("CN=" + objects, "group");
                                    newgroup.Properties["sAMAccountName"].Value = objects;

                                    var groupType = unchecked((int)(GroupType.UNIVERSAL | GroupType.SECURITY));
                                    //默认设置组为通用组
                                    newgroup.Properties["groupType"].Value = groupType;

                                    newgroup.CommitChanges();
                                    newgroup.Close();
                                    de.Close();
                                    isSuccess = true;
                                    message = new { message = objects + "新建成功。" };
                                }
                            }; break;
                        case "organizationalUnit":
                            {
                                if ((objects == string.Empty) || (oudn == string.Empty))
                                {
                                    message = new { message = objects + "参数不能为空。" };
                                }
                                else
                                {
                                    DirectoryEntry de = GetDirectoryObjectforOU(oudn, domain);
                                    DirectoryEntries Groups = de.Children;
                                    DirectoryEntry newgroup = Groups.Add("OU=" + objects, "organizationalUnit");
                                    //newgroup.Properties["sAMAccountName"].Value = groupname;
                                    newgroup.CommitChanges();
                                    //添加 防删除
                                    newgroup.RefreshCache();
                                    //NTAccount 域名\用户名
                                    IdentityReference ceveryOneAccount = new NTAccount("Everyone").Translate(typeof(SecurityIdentifier)); //S-1-1-0
                                    var cobjAce = new ActiveDirectoryAccessRule(ceveryOneAccount, ActiveDirectoryRights.Delete | ActiveDirectoryRights.DeleteTree, AccessControlType.Deny);
                                    var cobjACL = newgroup.ObjectSecurity;
                                    //set ace to object 设置对象对象
                                    cobjACL.AddAccessRule(cobjAce);
                                    //commit changes  提交更改
                                    newgroup.CommitChanges();
                                    var parentAce = new ActiveDirectoryAccessRule(ceveryOneAccount, ActiveDirectoryRights.DeleteChild, AccessControlType.Deny);
                                    de.ObjectSecurity.AddAccessRule(parentAce);
                                    //commit changes  提交更改
                                    de.CommitChanges();
                                    newgroup.Close();
                                    de.Close();
                                    isSuccess = true;
                                    message = new { message = objects + "新建成功。" };
                                }
                            }; break;
                        case "computer":
                            {
                                DirectoryEntry de = GetDirectoryObjectforOU(oudn, domain);
                                DirectoryEntries computers = de.Children;
                                DirectoryEntry newcomputer = computers.Add("CN=" + objects, "computer");//创建\
                                newcomputer.Properties["sAMAccountName"].Value = objects.ToUpper() + "$";
                                newcomputer.CommitChanges();
                                newcomputer.Properties["userAccountControl"].Value = 0x1000;//启用4096
                                newcomputer.CommitChanges();
                                newcomputer.Close();
                                de.Close();
                                isSuccess = true;
                                message = new { message = objects + "新建成功。" };
                            }; break;// 判断计算机是否存在
                        default: isSuccess = false; ; break;
                    }


                    var result = new { isSuccess = isSuccess, message = message };
                    HttpResponseMessage resultjson = toJson(result);
                    return resultjson;
                }
                catch (Exception ex)
                {
                    message = new { message = ex.Message };
                    var result = new { isSuccess = isSuccess, message = message };
                    HttpResponseMessage resultjson = toJson(result);
                    return resultjson;
                }
            }
            else
            {
                message = new { message = "API没经过授权无法调用!!!" };
                var result = new { isSuccess = isSuccess, message = message };
                HttpResponseMessage resultjson = toJson(result);
                return resultjson;
            }
        }

        #endregion

        #region (3)根据对象类别查询属性
        [HttpGet]
        public HttpResponseMessage GetobjectProperty(string objects, string objectClass, string skey, string domain)
        {
            var isSuccess = false;
            if (skey == admd5(domain))
            {
                try
                {

                    ArrayList mList = new ArrayList();
                    switch (objectClass)
                    {
                        case "user":
                            {
                                DirectoryEntry oUser = GetDirectoryEntryOfUser(objects, domain).GetDirectoryEntry();
                                oUser.CommitChanges();
                                var pwdset = GetDateTimeFromLargeInteger((IADsLargeInteger)oUser.Properties["pwdLastSet"].Value).ToString();//system.__comobject 先转换成IADsLargeInteger再转换成datatime
                                string PasswordExpirationDate = oUser.InvokeGet("PasswordExpirationDate").ToString(); //获取密码到期时间
                                if (PasswordExpirationDate == "1970/1/1 0:00:00")
                                {
                                    PasswordExpirationDate = "密码永不过期";
                                }
                                var aduser =
                                new
                                {
                                    cn = oUser.Properties["cn"].Value,
                                    name = oUser.Properties["name"].Value,
                                    sn = oUser.Properties["sn"].Value,//姓(L)
                                    givenName = oUser.Properties["givenName"].Value,//名(F)
                                    sAMAccountName = oUser.Properties["sAMAccountName"].Value,//账户登陆名(Windows 2000 以前版本)
                                    userPrincipalName = oUser.Properties["userPrincipalName"].Value,//账户登陆
                                    displayName = oUser.Properties["displayName"].Value, //显示名称
                                    wWWHomePage = oUser.Properties["wWWHomePage"].Value, //工号
                                    guid = oUser.Properties["physicalDeliveryOfficeName"].Value,//办公室(C)   
                                    description = oUser.Properties["description"].Value, //描述
                                    mail = oUser.Properties["mail"].Value, // 邮箱号
                                    distinguishedName = oUser.Properties["distinguishedName"].Value, // 位置
                                    homeMDB = oUser.Properties["homeMDB"].Value, // 用户邮箱号数据
                                    PasswordExpirationDate = PasswordExpirationDate, // 密码到期时间
                                    pwdLastSet = pwdset,//上次修改密码时间
                                    whenCreated = oUser.Properties["whenCreated"].Value.ToString(), // 用户创建时间
                                    whenChanged = oUser.Properties["whenChanged"].Value.ToString(), // 更新用户时间
                                    memberof = oUser.Properties["memberof"].Value, //用户权限
                                    proxyAddresses = oUser.Properties["proxyAddresses"].Value,//smtp
                                    userAccountControl = oUser.Properties["userAccountControl"].Value,//启用。禁用
                                    IsAccountLocked = userlock(objects, domain),  //0没有锁定，其他被锁定
                                };
                                oUser.Close();
                                mList.Add(aduser);
                                isSuccess = true;
                            }; break;
                        case "group":
                            {
                                DirectoryEntry oGroup = GetDirectoryEntryOfGroup(objects, domain).GetDirectoryEntry();
                                var aduser =
                                new
                                {
                                    cn = oGroup.Properties["cn"].Value,
                                    sAMAccountName = oGroup.Properties["sAMAccountName"].Value,//账户登陆名(Windows 2000 以前版本)
                                    distinguishedName = oGroup.Properties["distinguishedName"].Value, // 位置
                                    description = oGroup.Properties["description"].Value, // 描述
                                    whenCreated = oGroup.Properties["whenCreated"].Value.ToString(), // 创建时间
                                    whenChanged = oGroup.Properties["whenChanged"].Value.ToString(), // 更新时间
                                    memberof = oGroup.Properties["memberof"].Value, //隶属于
                                    member = oGroup.Properties["member"].Value, //组员
                                };
                                mList.Add(aduser);
                                isSuccess = true;
                            }; break;
                        case "organizationalUnit":
                            {
                                DirectoryEntry oOU = GetDirectoryObjectforOU(objects, domain);
                                var aduser =
                                new
                                {
                                    ou = oOU.Properties["ou"].Value,
                                    distinguishedName = oOU.Properties["distinguishedName"].Value, // 位置
                                    whenCreated = oOU.Properties["whenCreated"].Value.ToString(), // 创建时间
                                    whenChanged = oOU.Properties["whenChanged"].Value.ToString(), // 更新时间
                                };
                                mList.Add(aduser);
                                isSuccess = true;
                            }; break;
                        case "domain":
                            {
                                DirectoryEntry oOU = GetDirectoryObjectforOU(objects, domain);
                                var aduser =
                                new
                                {
                                    dc = oOU.Properties["dc"].Value,
                                    distinguishedName = oOU.Properties["distinguishedName"].Value, // 位置
                                    whenCreated = oOU.Properties["whenCreated"].Value.ToString(), // 创建时间
                                    whenChanged = oOU.Properties["whenChanged"].Value.ToString(), // 更新时间

                                };
                                mList.Add(aduser);
                                isSuccess = true;
                            }; break;
                        case "computer":
                            {
                                DirectoryEntry ocomputer = GetDirectoryEntryOfComputer(objects, domain).GetDirectoryEntry();
                                var aduser =
                                new
                                {
                                    cn = ocomputer.Properties["cn"].Value,
                                    sAMAccountName = ocomputer.Properties["sAMAccountName"].Value,
                                    distinguishedName = ocomputer.Properties["distinguishedName"].Value, // 位置
                                    userAccountControl = ocomputer.Properties["userAccountControl"].Value,
                                    AdmPwd = ocomputer.Properties["ms-Mcs-AdmPwd"].Value,
                                };
                                mList.Add(aduser);
                                isSuccess = true;
                            }; break;// 判断计算机是否存在
                        case "wWWHomePage":
                            {
                                DirectoryEntry job = GetDirectoryEntryByJobnumber(objects, domain).GetDirectoryEntry();
                                var pwdsetjob = GetDateTimeFromLargeInteger((IADsLargeInteger)job.Properties["pwdLastSet"].Value).ToString();//system.__comobject 先转换成IADsLargeInteger再转换成datatime
                                string PasswordExpirationDatejob = job.InvokeGet("PasswordExpirationDate").ToString(); //获取密码到期时间
                                if (PasswordExpirationDatejob == "1970/1/1 0:00:00")
                                {
                                    PasswordExpirationDatejob = "密码永不过期";
                                }
                                var aduser =
                                new
                                {
                                    cn = job.Properties["cn"].Value,
                                    name = job.Properties["name"].Value,
                                    sn = job.Properties["sn"].Value,//姓(L)
                                    givenName = job.Properties["givenName"].Value,//名(F)
                                    sAMAccountName = job.Properties["sAMAccountName"].Value,//账户登陆名(Windows 2000 以前版本)
                                    userPrincipalName = job.Properties["userPrincipalName"].Value,//账户登陆
                                    displayName = job.Properties["displayName"].Value, //显示名称
                                    wWWHomePage = job.Properties["wWWHomePage"].Value, //工号
                                    description = job.Properties["description"].Value, //描述
                                    guid = job.Properties["physicalDeliveryOfficeName"].Value,//办公室(C)   
                                    mail = job.Properties["mail"].Value, // 邮箱号
                                    distinguishedName = job.Properties["distinguishedName"].Value, // 位置
                                    homeMDB = job.Properties["homeMDB"].Value, // 用户邮箱号数据
                                    PasswordExpirationDate = PasswordExpirationDatejob, // 密码到期时间
                                    pwdLastSet = pwdsetjob,//上次修改密码时间
                                    whenCreated = job.Properties["whenCreated"].Value.ToString(), // 用户创建时间
                                    whenChanged = job.Properties["whenChanged"].Value.ToString(), // 更新用户时间
                                    memberof = job.Properties["memberof"].Value, //用户权限
                                    proxyAddresses = job.Properties["proxyAddresses"].Value,//smtp
                                    AdmPwd = job.Properties["ms-Mcs-AdmPwd"].Value,
                                    userAccountControl = job.Properties["userAccountControl"].Value,
                                    IsAccountLocked = userlock(objects, domain),
                                };
                                job.Close();
                                mList.Add(aduser);
                                isSuccess = true;
                            }; break;
                        default: isSuccess = false; ; break;
                    }
                    var result = new { isSuccess = isSuccess, message = mList };
                    HttpResponseMessage resultjson = toJson(result);
                    return resultjson;
                }
                catch (Exception ex)
                {
                    var message = new { message = ex.Message };
                    var result = new { isSuccess = isSuccess, message = message };
                    HttpResponseMessage resultjson = toJson(result);
                    return resultjson;
                }
            }
            else
            {
                var message = new { message = "API没经过授权无法调用!!!" };
                var result = new { isSuccess = isSuccess, message = message };
                HttpResponseMessage resultjson = toJson(result);
                return resultjson;
            }
        }

        #endregion

        #region (3.1)根据distinguishedName查询属性  区分类别
        [HttpGet]
        public HttpResponseMessage GetPropertyFordistinguishedName(string distinguishedName, string skey, string domain)
        {
            var isSuccess = false;
            if (skey == admd5(domain))
            {
                try
                {
                    ArrayList mList = new ArrayList();
                    DirectoryEntry oUser = GetDirectoryObjectforOU(distinguishedName, domain);
                    oUser.CommitChanges();
                    var objectClass = oUser.Properties["objectClass"];
                    if (objectClass.Contains("person") && objectClass.Contains("user"))
                    {
                        var pwdset = GetDateTimeFromLargeInteger((IADsLargeInteger)oUser.Properties["pwdLastSet"].Value).ToString();//system.__comobject 先转换成IADsLargeInteger再转换成datatime
                        string PasswordExpirationDate = oUser.InvokeGet("PasswordExpirationDate").ToString(); //获取密码到期时间
                        if (PasswordExpirationDate == "1970/1/1 0:00:00")
                        {
                            PasswordExpirationDate = "密码永不过期";
                        }
                        string sAMAccountName = oUser.Properties["sAMAccountName"].Value.ToString();
                        var aduser =
                        new
                        {
                            objectClass = oUser.Properties["objectClass"].Value,
                            cn = oUser.Properties["cn"].Value,
                            name = oUser.Properties["name"].Value,
                            sn = oUser.Properties["sn"].Value,//姓(L)
                            givenName = oUser.Properties["givenName"].Value,//名(F)
                            sAMAccountName = oUser.Properties["sAMAccountName"].Value,//账户登陆名(Windows 2000 以前版本)
                            userPrincipalName = oUser.Properties["userPrincipalName"].Value,//账户登陆
                            displayName = oUser.Properties["displayName"].Value, //显示名称
                            wWWHomePage = oUser.Properties["wWWHomePage"].Value, //工号
                            guid = oUser.Properties["physicalDeliveryOfficeName"].Value,//办公室(C)   
                            description = oUser.Properties["description"].Value, //描述
                            mail = oUser.Properties["mail"].Value, // 邮箱号
                            distinguishedName = oUser.Properties["distinguishedName"].Value, // 位置
                            homeMDB = oUser.Properties["homeMDB"].Value, // 用户邮箱号数据
                            PasswordExpirationDate = PasswordExpirationDate, // 密码到期时间
                            pwdLastSet = pwdset,//上次修改密码时间
                            whenCreated = oUser.Properties["whenCreated"].Value.ToString(), // 用户创建时间
                            whenChanged = oUser.Properties["whenChanged"].Value.ToString(), // 更新用户时间
                            memberof = oUser.Properties["memberof"].Value, //用户权限
                            proxyAddresses = oUser.Properties["proxyAddresses"].Value,//smtp
                            userAccountControl = oUser.Properties["userAccountControl"].Value,//启用。禁用
                            IsAccountLocked = userlock(sAMAccountName, domain),  //0没有锁定，其他被锁定
                        };
                        mList.Add(aduser);

                    }
                    else if (objectClass.Contains("group"))
                    {
                        var aduser =
                                new
                                {
                                    objectClass = oUser.Properties["objectClass"].Value,
                                    cn = oUser.Properties["cn"].Value,
                                    displayName = oUser.Properties["displayName"].Value, //显示名称
                                    sAMAccountName = oUser.Properties["sAMAccountName"].Value,//账户登陆名(Windows 2000 以前版本)
                                    distinguishedName = oUser.Properties["distinguishedName"].Value, // 位置
                                    description = oUser.Properties["description"].Value, // 描述
                                    whenCreated = oUser.Properties["whenCreated"].Value.ToString(), // 创建时间
                                    whenChanged = oUser.Properties["whenChanged"].Value.ToString(), // 更新时间
                                    memberof = oUser.Properties["memberof"].Value, //隶属于
                                    member = oUser.Properties["member"].Value, //组员
                                    mail = oUser.Properties["mail"].Value, //组员
                                };
                        mList.Add(aduser);
                    }
                    else
                    {
                        var aduser =
                                new
                                {
                                    objectClass = oUser.Properties["objectClass"].Value,
                                    distinguishedName = oUser.Properties["distinguishedName"].Value, // 位置
                                    whenCreated = oUser.Properties["whenCreated"].Value.ToString(), // 创建时间
                                    whenChanged = oUser.Properties["whenChanged"].Value.ToString(), // 更新时间
                                };
                        mList.Add(aduser);
                    }
                    oUser.Close();

                    isSuccess = true;
                    var result = new { isSuccess = isSuccess, message = mList };
                    HttpResponseMessage resultjson = toJson(result);
                    return resultjson;
                }
                catch (Exception ex)
                {
                    var message = new { message = ex.Message };
                    var result = new { isSuccess = isSuccess, message = message };
                    HttpResponseMessage resultjson = toJson(result);
                    return resultjson;
                }
            }
            else
            {
                var message = new { message = "API没经过授权无法调用!!!" };
                var result = new { isSuccess = isSuccess, message = message };
                HttpResponseMessage resultjson = toJson(result);
                return resultjson;
            }
        }
        #endregion

        #region (4)账号解锁  获取账户是否锁定 （没有锁定：0  ，锁定：ip）
        /// <summary>
        /// 账号解锁
        /// </summary>
        /// <param name="username">用户名</param>
        /// <param name="skey">秘钥</param>
        [HttpGet]
        public HttpResponseMessage UnlockAccount(string objects, string skey, string domain)
        {
            var isSuccess = false;
            if (skey == admd5(domain))
            {
                if (ObjectExists(objects, "user", domain))
                {
                    try
                    {
                        string ip = userlock(objects, domain);
                        if (ip == "0")
                        {
                            var message = new { message = objects + "没有锁定，请核实" };
                            var result = new { isSuccess = isSuccess, message = message };
                            HttpResponseMessage resultjson = toJson(result);
                            return resultjson;
                        }
                        else
                        {
                            DirectoryEntry oUser = GetDirectoryEntryOfUser(objects, ip, domain).GetDirectoryEntry();
                            oUser.InvokeSet("IsAccountLocked", false);
                            oUser.CommitChanges();
                            oUser.Close();
                            isSuccess = true;
                            var message = new { message = objects + "已成功解锁！" };
                            var result = new { isSuccess = isSuccess, message = message };
                            HttpResponseMessage resultjson = toJson(result);
                            return resultjson;
                        }

                    }
                    catch (Exception ex)
                    {
                        var message = new { message = "账号解锁失败，" + ex.Message };
                        var result = new { isSuccess = isSuccess, message = message };
                        HttpResponseMessage resultjson = toJson(result);
                        return resultjson;
                    }
                }
                else
                {
                    var message = new { message = objects + "，在AD域中不存在。" };
                    var result = new { isSuccess = isSuccess, message = message };
                    HttpResponseMessage resultjson = toJson(result);
                    return resultjson;
                }
            }
            else
            {
                var message = new { message = "API没经过授权无法调用。" };
                var result = new { isSuccess = isSuccess, message = message };
                HttpResponseMessage resultjson = toJson(result);
                return resultjson;
            }
        }

        public string userlock(string username, string domain)
        {
            try
            {
                ArrayList domainIps = new ArrayList();
                var message = string.Empty;
                Mysqldbinfo dbinfo = new Mysqldbinfo();
                Dictionary<string, string> sel_global = dbinfo.Selglobals(domain);
                try
                {
                    ArrayList SiteName_List = new ArrayList();
                    ArrayList IPAddress_List = new ArrayList();
                    DirectoryContext mycontext = new DirectoryContext(DirectoryContextType.Domain, domain, sel_global["ad_domain"] + "\\" + sel_global["ad_account"], sel_global["ad_password"]);
                    //DomainController dc = DomainController.FindOne(mycontext);
                    DomainControllerCollection dcs = DomainController.FindAll(mycontext);
                    foreach (DomainController dc in dcs)
                    {
                        string SiteName = dc.SiteName;
                        string IPAddress = dc.IPAddress;
                        if (SiteName_List.Contains(SiteName))
                        {

                        }
                        else
                        {
                            SiteName_List.Add(SiteName);
                            IPAddress_List.Add(IPAddress);
                        }
                    }
                    if (IPAddress_List.Count == 1)
                    {
                        domainIps.Add(sel_global["ad_ip"]);
                    }
                    else
                    {
                        domainIps = IPAddress_List;
                    }
                }
                catch (Exception)
                {
                    domainIps.Add(sel_global["ad_ip"]);
                }
                foreach (object domainIp in domainIps)
                {
                    string domain_Ip = domainIp.ToString();
                    try
                    {
                        DirectoryEntry de = GetDirectoryObjectIp(domain_Ip, domain);
                        DirectorySearcher deSearch = new DirectorySearcher(de);
                        deSearch.Filter = "(&(objectCategory=person)(objectClass=user)(sAMAccountName=" + username + ")(lockoutTime>=1))";
                        SearchResultCollection results = deSearch.FindAll();
                        if (results.Count != 0)
                        {
                            userlockvalue = 1;
                            message = domain_Ip;
                            break;
                        }
                        else
                        {
                            userlockvalue = 0;
                        }
                        de.Close();
                    }
                    catch (Exception)
                    {
                        userlockvalue = 0;
                    }
                }

                if (userlockvalue == 1)
                {
                    return message;
                }
                else
                {
                    message = "0";
                    return message;
                }
            }
            catch (Exception)
            {
                return "0";
            }


        }

        #endregion

        #region (5)修改用户属性
        /// <summary>
        ///  修改用户属性
        /// </summary>
        /// <param name="username"></param>
        /// <param name="PropertyName"></param>属性名称
        /// <param name="PropertyValue"></param>
        [HttpGet]
        public HttpResponseMessage SetuserProperty(string username, string PropertyName, string PropertyValue, string skey, string domain)
        {
            var isSuccess = false;
            if (skey == admd5(domain))
            {
                if (PropertyValue != null)
                {
                    try
                    {
                        if (ObjectExists(username, "user", domain))
                        {
                            DirectoryEntry oUser = GetDirectoryEntryOfUser(username, domain).GetDirectoryEntry();
                            oUser.CommitChanges();
                            if (oUser.Properties.Contains(PropertyName))
                            {
                                oUser.Properties[PropertyName][0] = PropertyValue;
                            }
                            else
                            {
                                oUser.Properties[PropertyName].Add(PropertyValue);
                            }
                            oUser.CommitChanges();
                            oUser.Close();
                            isSuccess = true;
                            var message = new { message = username + "的" + PropertyName + "属性，修改成功" };
                            var result = new { isSuccess = isSuccess, message = message };
                            HttpResponseMessage resultjson = toJson(result);
                            return resultjson;
                        }
                        else
                        {
                            var message = new { message = username + "，在AD中不存在。" };
                            var result = new { isSuccess = isSuccess, message = message };
                            HttpResponseMessage resultjson = toJson(result);
                            return resultjson;
                        }
                    }
                    catch (Exception ex)
                    {
                        var message = new { message = ex.Message };
                        var result = new { isSuccess = isSuccess, message = message };
                        HttpResponseMessage resultjson = toJson(result);
                        return resultjson;
                    }
                }
                else
                {
                    var message = new { message = PropertyValue + "不能为空" };
                    var result = new { isSuccess = isSuccess, message = message };
                    HttpResponseMessage resultjson = toJson(result);
                    return resultjson;
                }
            }
            else
            {
                var message = new { message = "API没经过授权无法调用!!!" };
                var result = new { isSuccess = isSuccess, message = message };
                HttpResponseMessage resultjson = toJson(result);
                return resultjson;
            }
        }

        #endregion

        #region (6)user密码重置，密码修改
        /// <summary>
        /// 密码修改
        /// </summary>
        /// <param name="username">用户名</param>
        /// <param name="oldpassword">原密码</param>
        /// <param name="newpassword">新密码</param>
        /// <param name="skey">秘钥</param>
        [HttpGet]
        public HttpResponseMessage ChangePassword(string username, string oldpassword, string newpassword, string skey, string domain)
        {
            var message = string.Empty;
            var isSuccess = false;
            if (skey == admd5(domain))
            {
                try
                {
                    if (username.ToLower() == "administrator")
                    {
                        message = "不能更改密码，administrator账号不能修改";
                    }
                    else
                    {
                        DirectoryEntry oUser = GetDirectoryEntryOfUser(username, domain).GetDirectoryEntry();
                        oUser.Invoke("ChangePassword", new Object[] { oldpassword, newpassword });
                        oUser.Properties["LockOutTime"].Value = 0; //unlock account
                        oUser.CommitChanges();
                        oUser.Close();
                        isSuccess = true;
                        message = username + "密码修改成功。";
                    }
                }
                catch (Exception ex)
                {
                    message = "不能更改密码，" + ex.Message;
                    Exception baseException = ex.GetBaseException();
                    if (baseException is COMException)
                    {
                        COMException comException = baseException as COMException;
                        switch (comException.ErrorCode)
                        {
                            case -2147024810:
                                message = "原密码输入错误。";
                                break;
                            case -2147022651:
                                message = "新密码密码不符合安全要求。";
                                break;
                            case -2147023570:
                                message = "用户或密码无效。";
                                break;
                            case -2147016657:
                                message = "用户或密码无效，请重试 ";
                                break;
                            default:
                                message = "unknown exception";
                                break;
                        }
                    }
                }
            }
            else
            {
                message = "API没经过授权无法调用!!!";
            }

            var result = new { isSuccess = isSuccess, message = message };
            HttpResponseMessage resultjson = toJson(result);
            return resultjson;
        }
        /// <summary>
        /// 密码重置
        /// </summary>
        /// <param name="username">用户名</param>
        /// <param name="newpassword">新密码</param>
        /// <param name="skey">秘钥</param>
        [HttpGet]
        public HttpResponseMessage ResetPasswordByOU(string username, string newpassword, string skey, string domain)
        {
            var isSuccess = false;
            if (skey == admd5(domain))
            {
                try
                {
                    if (username.ToLower() == "administrator")
                    {
                        var message = "不能更改密码，administrator账号不能修改";
                        var result = new { isSuccess = isSuccess, message = message };
                        HttpResponseMessage resultjson = toJson(result);
                        return resultjson;
                    }
                    else
                    {
                        DirectoryEntry oUser = GetDirectoryEntryOfUser(username, domain).GetDirectoryEntry();
                        oUser.Invoke("SetPassword", new Object[] { newpassword });
                        oUser.Properties["LockOutTime"].Value = 0; //unlock account
                        oUser.CommitChanges();
                        oUser.Close();
                        isSuccess = true;
                        var message = new { message = username + "密码重置成功。", newpassword = newpassword };
                        var result = new { isSuccess = isSuccess, message = message };
                        HttpResponseMessage resultjson = toJson(result);
                        return resultjson;
                    }
                }
                catch (Exception ex)
                {
                    var message = new { message = "不能重置密码，" + ex.Message };
                    Exception baseException = ex.GetBaseException();
                    if (baseException is COMException)
                    {
                        COMException comException = baseException as COMException;
                        switch (comException.ErrorCode)
                        {
                            case -2147022651:
                                message = new { message = "新密码密码不符合安全要求。" };
                                break;
                            case -2147023570:
                                message = new { message = "用户或密码无效。" };
                                break;
                            case -2147016657:
                                message = new { message = "用户或密码无效，请重试 。" };
                                break;
                            default:
                                message = new { message = "unknown exception" };
                                break;
                        }
                    }
                    var result = new { isSuccess = isSuccess, message = message };
                    HttpResponseMessage resultjson = toJson(result);
                    return resultjson;
                }
            }
            else
            {
                var message = new { message = "API没经过授权无法调用。" };
                var result = new { isSuccess = isSuccess, message = message };
                HttpResponseMessage resultjson = toJson(result);
                return resultjson;
            }
        }

        #endregion

        #region (7)根据对象类别移动到新OU
        [HttpGet]
        public HttpResponseMessage MoveToObject(string objects, string oudn, string objectClass, string skey, string domain)
        {
            var isSuccess = false;
            if (skey == admd5(domain))
            {
                try
                {
                    switch (objectClass)
                    {
                        case "user":
                            {
                                DirectoryEntry oUser = GetDirectoryEntryOfUser(objects, domain).GetDirectoryEntry();
                                DirectoryEntry de = GetDirectoryObjectforOU(oudn, domain);
                                oUser.MoveTo(de);
                                de.Close();
                                oUser.Close();
                                isSuccess = true;
                            }; break;

                        case "group":
                            {
                                DirectoryEntry oGroup = GetDirectoryEntryOfGroup(objects, domain).GetDirectoryEntry();
                                DirectoryEntry de = GetDirectoryObjectforOU(oudn, domain);
                                oGroup.MoveTo(de);
                                de.Close();
                                oGroup.Close();
                                isSuccess = true;
                            }; break;
                        case "organizationalUnit":
                            {
                                DirectoryEntry oOU = GetDirectoryObjectforOU(objects, domain);

                                oOU.RefreshCache();
                                IdentityReference everyOneAccount = new NTAccount("Everyone").Translate(typeof(SecurityIdentifier)); //S - 1 - 1 - 0
                                var objAce = new ActiveDirectoryAccessRule(everyOneAccount, ActiveDirectoryRights.Delete | ActiveDirectoryRights.DeleteTree, AccessControlType.Deny);
                                oOU.ObjectSecurity.RemoveAccessRule(objAce);
                                oOU.CommitChanges();
                                DirectoryEntry de = GetDirectoryObjectforOU(oudn, domain);
                                oOU.MoveTo(de);
                                oOU.ObjectSecurity.AddAccessRule(objAce);
                                oOU.CommitChanges();
                                var parentAce = new ActiveDirectoryAccessRule(everyOneAccount, ActiveDirectoryRights.DeleteChild, AccessControlType.Deny);
                                de.ObjectSecurity.AddAccessRule(parentAce);
                                de.CommitChanges();

                                de.Close();
                                oOU.Close();
                                isSuccess = true;
                            }; break;
                        case "computer":
                            {
                                DirectoryEntry ocomputer = GetDirectoryEntryOfComputer(objects, domain).GetDirectoryEntry();
                                DirectoryEntry de = GetDirectoryObjectforOU(oudn, domain);
                                ocomputer.MoveTo(de);
                                de.Close();
                                ocomputer.Close();
                                isSuccess = true;
                            }; break;// 判断计算机是否存在
                        case "wWWHomePage":
                            {
                                DirectoryEntry job = GetDirectoryEntryByJobnumber(objects, domain).GetDirectoryEntry();
                                DirectoryEntry de = GetDirectoryObjectforOU(oudn, domain);
                                job.MoveTo(de);
                                de.Close();
                                job.Close();
                                isSuccess = true;
                            }; break;

                        default: isSuccess = false; ; break;
                    }

                    var message = new { message = objects + "移动到：" + oudn };
                    var result = new { isSuccess = isSuccess, message = message };
                    HttpResponseMessage resultjson = toJson(result);
                    return resultjson;
                }
                catch (Exception ex)
                {
                    var message = new { message = ex.Message };
                    var result = new { isSuccess = isSuccess, message = message };
                    HttpResponseMessage resultjson = toJson(result);
                    return resultjson;
                }
            }
            else
            {
                var message = new { message = "API没经过授权无法调用!!!" };
                var result = new { isSuccess = isSuccess, message = message };
                HttpResponseMessage resultjson = toJson(result);
                return resultjson;
            }
        }
        #endregion

        #region (8)将用户加入到用户组中
        /// <summary>
        /// (3)将用户加入到用户组中
        /// </summary>
        /// <param name="username">用户名</param>
        /// <param name="groupname">组名</param>
        [HttpGet]
        public HttpResponseMessage AddUserToGroup(string sAMAccountName, string groupname, string skey, string domain)
        {
            var message = string.Empty;
            var isSuccess = false;
            if (skey == admd5(domain))
            {
                if ((groupname == string.Empty) || (sAMAccountName == string.Empty))
                {

                    message = "组名不能为空";
                }
                else
                {
                    if (ObjectExists(groupname, "group", domain))
                    {

                        try
                        {
                            if (ObjectExists(sAMAccountName, "user", domain))
                            {
                                DirectoryEntry oGroup = GetDirectoryEntryOfGroup(groupname, domain).GetDirectoryEntry();
                                DirectoryEntry oUser = GetDirectoryEntryOfUser(sAMAccountName, domain).GetDirectoryEntry();
                                oGroup.Properties["member"].Add(oUser.Properties["distinguishedName"].Value);
                                oGroup.CommitChanges();
                                oGroup.Close();
                                oUser.Close();
                                isSuccess = true;
                                message = sAMAccountName + ",在" + groupname + "中添加成功。";
                            }
                            else if (ObjectExists(sAMAccountName, "group", domain))
                            {
                                DirectoryEntry oGroup = GetDirectoryEntryOfGroup(groupname, domain).GetDirectoryEntry();
                                DirectoryEntry oUser = GetDirectoryEntryOfGroup(sAMAccountName, domain).GetDirectoryEntry();
                                oGroup.Properties["member"].Add(oUser.Properties["distinguishedName"].Value);
                                oGroup.CommitChanges();
                                oGroup.Close();
                                oUser.Close();
                                isSuccess = true;
                                message = sAMAccountName + ",在" + groupname + "中添加成功。";
                            }
                            else
                            {
                                message = sAMAccountName + "域中不存在；";
                            }

                        }
                        catch (Exception ex)
                        {
                            message = sAMAccountName + ex.Message;
                        }
                    }
                    else
                    {
                        message += groupname + "AD域中不存在或者输入有误；";
                    }
                }
            }
            else
            {
                message = "API没经过授权无法调用!!!";
            }
            var result = new { isSuccess = isSuccess, message = message };
            HttpResponseMessage resultjson = toJson(result);
            return resultjson;

        }
        #endregion

        #region (9)将用户从组中移除
        /// <summary>
        /// (4)将用户从组中移除
        /// </summary>
        /// <param name="username">用户名</param>
        /// <param name="groupname">组名</param>
        [HttpGet]
        public HttpResponseMessage RemoveUserFromGroup(string sAMAccountName, string groupname, string skey, string domain)
        {
            var message = string.Empty;
            var isSuccess = false;
            if (skey == admd5(domain))
            {
                if ((groupname == string.Empty) || (sAMAccountName == string.Empty))
                {

                    message = "组名不能为空";
                }
                else
                {
                    if (ObjectExists(groupname, "group", domain))
                    {
                        try
                        {
                            if (ObjectExists(sAMAccountName, "user", domain))
                            {
                                DirectoryEntry oGroup = GetDirectoryEntryOfGroup(groupname, domain).GetDirectoryEntry();
                                DirectoryEntry oUser = GetDirectoryEntryOfUser(sAMAccountName, domain).GetDirectoryEntry();
                                oGroup.Properties["member"].Remove(oUser.Properties["distinguishedName"].Value);
                                oGroup.CommitChanges();
                                oGroup.Close();
                                oUser.Close();
                                isSuccess = true;
                                message = sAMAccountName + ",在" + groupname + "移除成功。";
                            }
                            else if (ObjectExists(sAMAccountName, "group", domain))
                            {
                                DirectoryEntry oGroup = GetDirectoryEntryOfGroup(groupname, domain).GetDirectoryEntry();
                                DirectoryEntry oUser = GetDirectoryEntryOfGroup(sAMAccountName, domain).GetDirectoryEntry();
                                oGroup.Properties["member"].Remove(oUser.Properties["distinguishedName"].Value);
                                oGroup.CommitChanges();
                                oGroup.Close();
                                oUser.Close();
                                isSuccess = true;
                                message = sAMAccountName + ",在" + groupname + "移除成功。";
                            }
                            else
                            {
                                message = sAMAccountName + "域中不存在；";
                            }
                        }
                        catch (Exception ex)
                        {
                            message = sAMAccountName + ex.Message;

                        }
                    }
                    else
                    {
                        message += groupname + "AD域中不存在或者输入有误；";
                    }
                }
            }
            else
            {
                message = "API没经过授权无法调用!!!";
            }
            var result = new { isSuccess = isSuccess, message = message };
            HttpResponseMessage resultjson = toJson(result);
            return resultjson;
        }
        #endregion

        #region (10)从用户组中获得组员
        /// <summary>
        /// (5)从用户组中获得组员
        /// </summary>
        /// <param name="groupname">组名</param>
        [HttpGet]
        public HttpResponseMessage GetUserFromGroup(string groupname, string skey, string domain)
        {
            var isSuccess = false;
            if (skey == admd5(domain))
            {
                try
                {
                    if (ObjectExists(groupname, "group", domain))
                    {
                        DirectoryEntry oGroup = GetDirectoryEntryOfGroup(groupname, domain).GetDirectoryEntry();
                        int n = oGroup.Properties["member"].Count;
                        if (n > 0)
                        {
                            string[] member = new string[n];
                            List<object> Group = new List<object>();
                            int i = 0;
                            foreach (object myColl in oGroup.Properties["member"])
                            {
                                member[i] = myColl.ToString().Substring(3, myColl.ToString().IndexOf(",") - 3);
                                var aduser =
                                    new
                                    {
                                        name = member[i],
                                        member = myColl,

                                    };
                                Group.Add(aduser);
                                i++;
                            }
                            oGroup.Close();
                            isSuccess = true;
                            var message = new { message = Group };
                            var result = new { isSuccess = isSuccess, message = message };
                            HttpResponseMessage resultjson = toJson(result);
                            return resultjson;
                        }
                        else
                        {
                            var message = new { message = "没有成员!" };
                            var result = new { isSuccess = isSuccess, message = message };
                            HttpResponseMessage resultjson = toJson(result);
                            return resultjson;
                        }
                    }
                    else
                    {
                        var message = new { message = "找不到此群组!" };
                        var result = new { isSuccess = isSuccess, message = message };
                        HttpResponseMessage resultjson = toJson(result);
                        return resultjson;
                    }
                }
                catch (Exception ex)
                {
                    var message = new { message = ex.Message };
                    var result = new { isSuccess = isSuccess, message = message };
                    HttpResponseMessage resultjson = toJson(result);
                    return resultjson;
                }

            }
            else
            {
                var message = new { message = "API没经过授权无法调用!!!" };
                var result = new { isSuccess = isSuccess, message = message };
                HttpResponseMessage resultjson = toJson(result);
                return resultjson;
            }
        }
        #endregion

        #region (11)移除组中所有成员
        /// <summary>
        /// 移除组中所有成员
        /// </summary>
        /// <param name="groupname">用户名</param>
        /// <param name="skey">秘钥</param>
        [HttpGet]
        public HttpResponseMessage RemoveAllUserFromGroup(string groupname, string skey, string domain)
        {
            var isSuccess = false;
            if (skey == admd5(domain))
            {
                if (ObjectExists(groupname, "group", domain))
                {
                    try
                    {
                        DirectoryEntry oGroup = GetDirectoryEntryOfGroup(groupname, domain).GetDirectoryEntry();
                        System.DirectoryServices.PropertyCollection pcoll = oGroup.Properties;
                        int n = pcoll["member"].Count;
                        List<object> User = new List<object>();
                        var member = string.Empty;
                        for (int i = 0; i < n; i++)
                        {
                            //                            string username = pcoll["member"][l].ToString()
                            //                                .Substring(3, pcoll["member"][l].ToString().IndexOf(",") - 3);
                            //                            DirectoryEntry oUser = GetDirectoryEntryOfUser(username).GetDirectoryEntry();
                            //                            string userDn = GetProperty(oUser, "distinguishedName");

                            while (oGroup.Properties["member"].Count > 0)
                            {
                                object membercoll = oGroup.Properties["member"][i];
                                member = membercoll.ToString().Substring(3, membercoll.ToString().IndexOf(",") - 3);
                                User.Add(member);
                                oGroup.Properties["member"].Remove(oGroup.Properties["member"][i]);
                                oGroup.CommitChanges();
                            }
                        }
                        oGroup.Close();
                        isSuccess = true;
                        var message = new { message = groupname + "中的组员全部移除！", removeuser = User };
                        var result = new { isSuccess = isSuccess, message = message };
                        HttpResponseMessage resultjson = toJson(result);
                        return resultjson;
                    }
                    catch (Exception ex)
                    {
                        var message = new { message = ex.Message };
                        var result = new { isSuccess = isSuccess, message = message };
                        HttpResponseMessage resultjson = toJson(result);
                        return resultjson;
                    }

                }
                else
                {
                    var message = new { message = groupname + "AD域中不存在或者输入有误；" };
                    var result = new { isSuccess = isSuccess, message = message };
                    HttpResponseMessage resultjson = toJson(result);
                    return resultjson;
                }

            }
            else
            {
                var message = new { message = "API没经过授权无法调用!!!" };
                var result = new { isSuccess = isSuccess, message = message };
                HttpResponseMessage resultjson = toJson(result);
                return resultjson;
            }

        }
        #endregion

        #region (12)根据用户名获取用户所有组(权限）
        /// <summary>
        /// 根据用户名获取用户所有组
        /// </summary>
        /// <param name="username"></param>
        /// <returns>返回AD用户所有组</returns>
        [HttpGet]
        public HttpResponseMessage GetAdGroup(string username, string skey, string domain)
        {
            var isSuccess = false;
            if (skey == admd5(domain))
            {
                if (ObjectExists(username, "user", domain))
                {
                    try
                    {
                        DirectoryEntry oUser = GetDirectoryEntryOfUser(username, domain).GetDirectoryEntry();
                        int n = oUser.Properties["memberof"].Count;
                        string[] memberof = new string[n];
                        int i = 0;
                        foreach (object myColl in oUser.Properties["memberof"])
                        {
                            memberof[i] = myColl.ToString();
                            i++;
                        }
                        var userofgroup =
                                new
                                {
                                    adaccount = username,
                                    groups = memberof
                                };
                        oUser.Close();
                        isSuccess = true;
                        var result = new { isSuccess = isSuccess, message = userofgroup };
                        HttpResponseMessage resultjson = toJson(result);
                        return resultjson;
                    }
                    catch (Exception ex)
                    {
                        var message = new { message = ex.Message };
                        var result = new { isSuccess = isSuccess, message = message };
                        HttpResponseMessage resultjson = toJson(result);
                        return resultjson;
                    }
                }
                else
                {
                    var message = new { message = username + "，在AD中不存在。" };
                    var result = new { isSuccess = isSuccess, message = message };
                    HttpResponseMessage resultjson = toJson(result);
                    return resultjson;
                }
            }
            else
            {
                var message = new { message = "API没经过授权无法调用!!!" };
                var result = new { isSuccess = isSuccess, message = message };
                HttpResponseMessage resultjson = toJson(result);
                return resultjson;
            }

        }
        #endregion


        #region(13)根据工号获取AD账号，姓名，邮箱） 
        [HttpGet]
        public HttpResponseMessage GetAccountinfoByJobnumber(string jobnumber, string skey, string domain)
        {
            var isSuccess = false;
            if (skey == admd5(domain))
            {
                try
                {
                    DirectoryEntry oUser = GetDirectoryEntryByJobnumber(jobnumber, domain).GetDirectoryEntry();
                    var pwdset = GetDateTimeFromLargeInteger((IADsLargeInteger)oUser.Properties["pwdLastSet"].Value).ToString();//system.__comobject 先转换成IADsLargeInteger再转换成datatime
                    string PasswordExpirationDate = oUser.InvokeGet("PasswordExpirationDate").ToString(); //获取密码到期时间
                    if (PasswordExpirationDate == "1970/1/1 0:00:00")
                    {
                        PasswordExpirationDate = "密码永不过期";
                    }
                    var aduser =
                    new
                    {
                        cn = oUser.Properties["cn"].Value,
                        name = oUser.Properties["name"].Value,
                        sn = oUser.Properties["sn"].Value,//姓(L)
                        givenName = oUser.Properties["givenName"].Value,//名(F)
                        sAMAccountName = oUser.Properties["sAMAccountName"].Value,//账户登陆名(Windows 2000 以前版本)
                        userPrincipalName = oUser.Properties["userPrincipalName"].Value,//账户登陆
                        displayname = oUser.Properties["displayName"].Value, //显示名称
                        jobnumber = oUser.Properties["wWWHomePage"].Value, //工号
                        description = oUser.Properties["description"].Value, //描述
                        guid = oUser.Properties["physicalDeliveryOfficeName"].Value, //guid
                        mail = oUser.Properties["mail"].Value, // 邮箱号
                        distinguishedName = oUser.Properties["distinguishedName"].Value, // 位置
                        maildb = oUser.Properties["homeMDB"].Value, // 用户邮箱号数据
                        passwordExpria = PasswordExpirationDate, // 密码到期时间
                        pwdset = pwdset,//上次修改密码时间
                        whenCreated = oUser.Properties["whenCreated"].Value.ToString(), // 用户创建时间
                        whenChanged = oUser.Properties["whenChanged"].Value.ToString(), // 更新用户时间
                        memberof = oUser.Properties["memberof"].Value, //用户权限
                        proxyAddresses = oUser.Properties["proxyAddresses"].Value, //SMTP
                        userAccountControl = oUser.Properties["userAccountControl"].Value,//启用。禁用
                    };
                    oUser.Close();
                    isSuccess = true;
                    var result = new { isSuccess = isSuccess, message = aduser };
                    HttpResponseMessage resultjson = toJson(result);
                    return resultjson;
                }
                catch (Exception ex)
                {

                    var message = new { message = ex.Message };
                    var result = new { isSuccess = isSuccess, message = message };
                    HttpResponseMessage resultjson = toJson(result);
                    return resultjson;
                }
            }
            else
            {
                var message = new { message = "API没经过授权无法调用!!!" };
                var result = new { isSuccess = isSuccess, message = message };
                HttpResponseMessage resultjson = toJson(result);
                return resultjson;
            }

        }
        #endregion

        #region(14)根据Gid获取AD账号，姓名，邮箱）
        [HttpGet]
        public HttpResponseMessage GetAccountinfoByGid(string guid, string skey, string domain)
        {
            var isSuccess = false;
            if (skey == admd5(domain))
            {
                try
                {
                    DirectoryEntry oUser = GetDirectoryEntryByGid(guid, domain).GetDirectoryEntry();
                    var pwdset = GetDateTimeFromLargeInteger((IADsLargeInteger)oUser.Properties["pwdLastSet"].Value).ToString();//system.__comobject 先转换成IADsLargeInteger再转换成datatime
                    string PasswordExpirationDate = oUser.InvokeGet("PasswordExpirationDate").ToString(); //获取密码到期时间
                    if (PasswordExpirationDate == "1970/1/1 0:00:00")
                    {
                        PasswordExpirationDate = "密码永不过期";
                    }
                    var aduser =
                    new
                    {
                        cn = oUser.Properties["cn"].Value,
                        name = oUser.Properties["name"].Value,
                        sn = oUser.Properties["sn"].Value,//姓(L)
                        givenName = oUser.Properties["givenName"].Value,//名(F)
                        sAMAccountName = oUser.Properties["sAMAccountName"].Value,//账户登陆名(Windows 2000 以前版本)
                        userPrincipalName = oUser.Properties["userPrincipalName"].Value,//账户登陆
                        displayname = oUser.Properties["displayName"].Value, //显示名称
                        jobnumber = oUser.Properties["wWWHomePage"].Value, //工号
                        description = oUser.Properties["description"].Value, //描述
                        guid = oUser.Properties["physicalDeliveryOfficeName"].Value, //guid
                        mail = oUser.Properties["mail"].Value, // 邮箱号
                        distinguishedName = oUser.Properties["distinguishedName"].Value, // 位置
                        maildb = oUser.Properties["homeMDB"].Value, // 用户邮箱号数据
                        passwordExpria = PasswordExpirationDate, // 密码到期时间
                        pwdset = pwdset,//上次修改密码时间
                        whenCreated = oUser.Properties["whenCreated"].Value.ToString(), // 用户创建时间
                        whenChanged = oUser.Properties["whenChanged"].Value.ToString(), // 更新用户时间
                        memberof = oUser.Properties["memberof"].Value, //用户权限
                        proxyAddresses = oUser.Properties["proxyAddresses"].Value, //SMTP
                        userAccountControl = oUser.Properties["userAccountControl"].Value,//启用。禁用

                    };
                    oUser.Close();
                    isSuccess = true;
                    var result = new { isSuccess = isSuccess, message = aduser };
                    HttpResponseMessage resultjson = toJson(result);
                    return resultjson;
                }
                catch (Exception ex)
                {

                    var message = new { message = ex.Message };
                    var result = new { isSuccess = isSuccess, message = message };
                    HttpResponseMessage resultjson = toJson(result);
                    return resultjson;
                }
            }
            else
            {
                var message = new { message = "API没经过授权无法调用!!!" };
                var result = new { isSuccess = isSuccess, message = message };
                HttpResponseMessage resultjson = toJson(result);
                return resultjson;
            }

        }
        #endregion

        #region(14)根据Dis获取AD账号，姓名，邮箱）
        [HttpGet]
        public HttpResponseMessage GetAccountinfoByDis(string displayname, string skey, string domain)
        {
            var isSuccess = false;
            if (skey == admd5(domain))
            {
                try
                {
                    DirectoryEntry oUser = GetDirectoryEntryByDis(displayname, domain).GetDirectoryEntry();
                    var pwdset = GetDateTimeFromLargeInteger((IADsLargeInteger)oUser.Properties["pwdLastSet"].Value).ToString();//system.__comobject 先转换成IADsLargeInteger再转换成datatime
                    string PasswordExpirationDate = oUser.InvokeGet("PasswordExpirationDate").ToString(); //获取密码到期时间
                    if (PasswordExpirationDate == "1970/1/1 0:00:00")
                    {
                        PasswordExpirationDate = "密码永不过期";
                    }
                    var aduser =
                    new
                    {
                        cn = oUser.Properties["cn"].Value,
                        name = oUser.Properties["name"].Value,
                        sn = oUser.Properties["sn"].Value,//姓(L)
                        givenName = oUser.Properties["givenName"].Value,//名(F)
                        sAMAccountName = oUser.Properties["sAMAccountName"].Value,//账户登陆名(Windows 2000 以前版本)
                        userPrincipalName = oUser.Properties["userPrincipalName"].Value,//账户登陆
                        displayname = oUser.Properties["displayName"].Value, //显示名称
                        jobnumber = oUser.Properties["wWWHomePage"].Value, //工号
                        description = oUser.Properties["description"].Value, //描述
                        guid = oUser.Properties["physicalDeliveryOfficeName"].Value, //guid
                        mail = oUser.Properties["mail"].Value, // 邮箱号
                        distinguishedName = oUser.Properties["distinguishedName"].Value, // 位置
                        maildb = oUser.Properties["homeMDB"].Value, // 用户邮箱号数据
                        passwordExpria = PasswordExpirationDate, // 密码到期时间
                        pwdset = pwdset,//上次修改密码时间
                        whenCreated = oUser.Properties["whenCreated"].Value.ToString(), // 用户创建时间
                        whenChanged = oUser.Properties["whenChanged"].Value.ToString(), // 更新用户时间
                        memberof = oUser.Properties["memberof"].Value, //用户权限
                        proxyAddresses = oUser.Properties["proxyAddresses"].Value,//smtp
                        userAccountControl = oUser.Properties["userAccountControl"].Value,//启用。禁用

                    };
                    oUser.Close();
                    isSuccess = true;
                    var result = new { isSuccess = isSuccess, message = aduser };
                    HttpResponseMessage resultjson = toJson(result);
                    return resultjson;
                }
                catch (Exception ex)
                {

                    var message = new { message = ex.Message };
                    var result = new { isSuccess = isSuccess, message = message };
                    HttpResponseMessage resultjson = toJson(result);
                    return resultjson;
                }
            }
            else
            {
                var message = new { message = "API没经过授权无法调用!!!" };
                var result = new { isSuccess = isSuccess, message = message };
                HttpResponseMessage resultjson = toJson(result);
                return resultjson;
            }

        }
        #endregion

        #region(15)测试加密
        [HttpGet]
        public HttpResponseMessage Encryption(string guid)
        {

            Mysqldbinfo dbinfo = new Mysqldbinfo();
            string ske = dbinfo.Encryption1(guid);
            var result = new { isSuccess = true, message = ske };
            HttpResponseMessage resultjson = toJson(result);
            return resultjson;


        }
        #endregion

        #region(15)测试解密
        public HttpResponseMessage Decrypt(string guid, string name)
        {
            var result = new { isSuccess = false, message = "meiy" };
            if (name == "adminuser")
            {
                Mysqldbinfo dbinfo = new Mysqldbinfo();
                string ske = dbinfo.Decrypt1(guid);
                result = new { isSuccess = true, message = ske };

            }
            HttpResponseMessage resultjson = toJson(result);
            return resultjson;
        }
        #endregion

        #region (16)根据用户名和密码确定权限
        /// <summary>
        /// 
        /// </summary>
        /// <param name="username"></param>
        /// <param name="password"></param>
        /// <param name="skey"></param>
        /// <param name="domain"></param>
        /// <returns></returns>
        [HttpGet]
        public HttpResponseMessage VerifyUserLogin(string username, string password, string skey, string domain)
        {
            var isSuccess = false;
            if (skey == admd5(domain))
            {
                if (ObjectExists(username, "user", domain))
                {
                    if (VerifyUserLogin(username, password, domain))
                    {
                        try
                        {
                            DirectoryEntry oUser = GetDirectoryEntryOfUser(username, domain).GetDirectoryEntry();
                            var message =
                                new
                                {
                                    name = oUser.Properties["displayName"].Value,
                                    jobnumber = oUser.Properties["wWWHomePage"].Value,
                                    mail = oUser.Properties["mail"].Value,
                                    guid = oUser.Properties["physicalDeliveryOfficeName"].Value,
                                    DN = oUser.Properties["distinguishedName"].Value,
                                    givenName = oUser.Properties["givenName"].Value,
                                    description = oUser.Properties["description"].Value,
                                    sn = oUser.Properties["sn"].Value
                                };
                            oUser.Close();
                            isSuccess = true;
                            var result = new { isSuccess = isSuccess, message = message };
                            HttpResponseMessage resultjson = toJson(result);
                            return resultjson;
                        }
                        catch (Exception ex)
                        {
                            var message = new { message = ex.Message };
                            var result = new { isSuccess = isSuccess, message = message };
                            HttpResponseMessage resultjson = toJson(result);
                            return resultjson;
                        }
                    }
                    else
                    {
                        var message =
                                new
                                {
                                    message = "用户名或者密码不正确"
                                };
                        var result = new { isSuccess = isSuccess, message = message };
                        HttpResponseMessage resultjson = toJson(result);
                        return resultjson;
                    }
                }
                else
                {
                    var message =
                            new
                            {
                                message = "用户不存在"
                            };
                    var result = new { isSuccess = isSuccess, message = message };
                    HttpResponseMessage resultjson = toJson(result);
                    return resultjson;
                }
            }
            else
            {
                var message = new { message = "API没经过授权无法调用!!!" };
                var result = new { isSuccess = isSuccess, message = message };
                HttpResponseMessage resultjson = toJson(result);
                return resultjson;
            }
        }
        #endregion

        #region (17)设置OU进行删除组 
        /// <summary>
        /// (6)设置OU进行删除组
        /// </summary>
        /// <param name="groupname">AD组名</param>
        /// <param name="ou">ou</param>,
        /// <param name="skey">秘钥</param>
        [HttpGet]
        public HttpResponseMessage DeleteAdgroupByOU(string groupname, string ou, string skey, string domain)
        {
            var isSuccess = false;
            if (skey == admd5(domain))
            {
                if (ObjectExists(groupname, "group", domain))
                {
                    try
                    {
                        if (ObjectExistsOU(groupname, "group", ou, domain))
                        {
                            DirectoryEntry oGroup = GetDirectoryEntryOfGroup(groupname, domain).GetDirectoryEntry();
                            oGroup.DeleteTree();
                            oGroup.Close();
                            isSuccess = true;
                            var message = new { message = groupname + "，删除成功！" };
                            var result = new { isSuccess = isSuccess, message = message };
                            HttpResponseMessage resultjson = toJson(result);
                            return resultjson;
                        }
                        else
                        {
                            var message = new { message = "此账号无法删除！！！" };
                            var result = new { isSuccess = isSuccess, message = message };
                            HttpResponseMessage resultjson = toJson(result);
                            return resultjson;
                        }
                    }
                    catch (Exception ex)
                    {
                        var message = new { message = ex.Message };
                        var result = new { isSuccess = isSuccess, message = message };
                        HttpResponseMessage resultjson = toJson(result);
                        return resultjson;
                    }
                }
                else
                {
                    var message = new { message = groupname + "，在OU=" + ou + "中不存在。" };
                    var result = new { isSuccess = isSuccess, message = message };
                    HttpResponseMessage resultjson = toJson(result);
                    return resultjson;
                }
            }
            else
            {
                var message = new { message = "API没经过授权无法调用!!!" };
                var result = new { isSuccess = isSuccess, message = message };
                HttpResponseMessage resultjson = toJson(result);
                return resultjson;
            }
        }
        #endregion

        #region (18)判断OU下是否有任何对象
        [HttpGet]
        public HttpResponseMessage inspectOU(string ouname, string skey, string domain)
        {
            var isSuccess = false;
            if (skey == admd5(domain))
            {

                try
                {
                    if (ouname == string.Empty || ouname == null)
                    {
                        var message = new { message = ouname + "不能为空" };
                        var result = new { isSuccess = isSuccess, message = message };
                        HttpResponseMessage resultjson = toJson(result);
                        return resultjson;
                    }
                    else
                    {
                        DirectoryEntry ou = GetDirectoryObjectforOU(ouname, domain);
                        ou.CommitChanges();
                        DirectorySearcher deSearchs = new DirectorySearcher(ou);
                        var a = deSearchs.FindAll().Count;
                        if (a != 1)
                        {
                            string PInfo = "";
                            foreach (SearchResult resEnt in deSearchs.FindAll())
                            {
                                DirectoryEntry myDirectoryEntry = resEnt.GetDirectoryEntry();
                                PInfo += myDirectoryEntry.Properties["name"].Value + ",";
                            }
                            isSuccess = true;
                            var message = new { message = ouname + "，里面有" + PInfo + "对象！" };
                            var result = new { isSuccess = isSuccess, message = message };
                            HttpResponseMessage resultjson = toJson(result);
                            return resultjson;
                        }
                        else
                        {
                            var message = new { message = ouname + "，里面没有任何对象" };
                            var result = new { isSuccess = isSuccess, message = message };
                            HttpResponseMessage resultjson = toJson(result);
                            return resultjson;
                        }
                    }
                }
                catch (Exception ex)
                {
                    var message = new { message = ex.Message };
                    var result = new { isSuccess = isSuccess, message = message };
                    HttpResponseMessage resultjson = toJson(result);
                    return resultjson;
                }
            }
            else
            {
                var message = new { message = "API没经过授权无法调用!!!" };
                var result = new { isSuccess = isSuccess, message = message };
                HttpResponseMessage resultjson = toJson(result);
                return resultjson;
            }
        }
        #endregion

        #region (19)设置OU进行删除OU 固定,当OU里面有对象无法删除
        /// <summary>
        /// (13)设置OU进行删除OU
        /// </summary>
        /// <param name="groupname">AD组名</param>
        /// <param name="ou">ou</param>
        /// <param name="skey">秘钥</param>
        [HttpGet]
        public HttpResponseMessage DeleteAdouByOU(string ouname, string ou, string skey, string domain)
        {
            var isSuccess = false;
            if (skey == admd5(domain))
            {
                try
                {
                    if (ou == string.Empty || ouname == string.Empty || ouname == null || ou == null)
                    {
                        var message = new { message = ou + "或" + ouname + "不能为空" };
                        var result = new { isSuccess = isSuccess, message = message };
                        HttpResponseMessage resultjson = toJson(result);
                        return resultjson;
                    }
                    else
                    {
                        List<string> ounamelist = new List<string>(ouname.Split(','));
                        string ounamestr = ounamelist[0].Replace("OU=", "");
                        if (ObjectExistsOU(ounamestr, "organizationalUnitSubtree", ou, domain))
                        {
                            if (ouname.Contains(ou))
                            {
                                DirectoryEntry delou = GetDirectoryObjectforOU(ouname, domain);
                                DirectorySearcher deSearch = new DirectorySearcher(delou);
                                var a = deSearch.FindAll().Count;
                                if (a == 1)
                                {
                                    delou.RefreshCache();
                                    IdentityReference everyOneAccount = new NTAccount("Everyone").Translate(typeof(SecurityIdentifier)); //S - 1 - 1 - 0
                                    var objAce = new ActiveDirectoryAccessRule(everyOneAccount, ActiveDirectoryRights.Delete | ActiveDirectoryRights.DeleteTree, AccessControlType.Deny);
                                    //set ace to object 设置对象对象    移除防删除                     
                                    delou.ObjectSecurity.RemoveAccessRule(objAce);
                                    delou.CommitChanges();
                                    delou.DeleteTree();
                                    delou.Close();

                                    isSuccess = true;
                                    var message = new { message = ouname + "，删除成功！" };
                                    var result = new { isSuccess = isSuccess, message = message };
                                    HttpResponseMessage resultjson = toJson(result);
                                    return resultjson;
                                }
                                else
                                {
                                    string PInfo = "";
                                    foreach (SearchResult resEnt in deSearch.FindAll())
                                    {
                                        DirectoryEntry myDirectoryEntry = resEnt.GetDirectoryEntry();
                                        PInfo += myDirectoryEntry.Properties["name"].Value + ",";
                                    }
                                    delou.Close();
                                    var message = new { message = ouname + "，里面有" + PInfo + "对象无法删除！" };
                                    var result = new { isSuccess = isSuccess, message = message };
                                    HttpResponseMessage resultjson = toJson(result);
                                    return resultjson;
                                }
                            }
                            else
                            {
                                var message = new { ouname = ouname, ou = ou, message = "ouname不在ou,里面" };
                                var result = new { isSuccess = isSuccess, message = message };
                                HttpResponseMessage resultjson = toJson(result);
                                return resultjson;
                            }

                        }
                        else
                        {
                            var message = new { message = "此账号无法删除！！！" };
                            var result = new { isSuccess = isSuccess, message = message };
                            HttpResponseMessage resultjson = toJson(result);
                            return resultjson;
                        }
                    }
                }
                catch (Exception ex)
                {
                    var message = new { message = ex.Message };
                    var result = new { isSuccess = isSuccess, message = message };
                    HttpResponseMessage resultjson = toJson(result);
                    return resultjson;
                }

            }
            else
            {
                var message = new { message = "API没经过授权无法调用!!!" };
                var result = new { isSuccess = isSuccess, message = message };
                HttpResponseMessage resultjson = toJson(result);
                return resultjson;
            }
        }
        #endregion

        #region (20)根据对象类别重命名
        [HttpGet]
        public HttpResponseMessage Renameobject(string objects, string newobjects, string objectClass, string skey, string domain)
        {
            var isSuccess = false;
            if (skey == admd5(domain))
            {
                try
                {
                    Mysqldbinfo dbinfo = new Mysqldbinfo();
                    var sel = dbinfo.Selglobals(domain);
                    switch (objectClass)
                    {
                        case "user":
                            {
                                DirectoryEntry oUser = GetDirectoryEntryOfUser(objects, domain).GetDirectoryEntry();
                                oUser.Properties["sAMAccountName"][0] = newobjects;
                                oUser.CommitChanges();
                                oUser.Properties["userPrincipalName"][0] = (newobjects + sel["fulldomain"]);
                                oUser.CommitChanges();
                                oUser.Rename("cn=" + newobjects);
                                oUser.CommitChanges();
                                oUser.Close();
                                isSuccess = true;
                            }; break;

                        case "group":
                            {
                                DirectoryEntry oGroup = GetDirectoryEntryOfGroup(objects, domain).GetDirectoryEntry();
                                oGroup.Properties["sAMAccountName"][0] = newobjects;
                                oGroup.CommitChanges();
                                oGroup.Rename("cn=" + newobjects);
                                oGroup.CommitChanges();
                                oGroup.Close();

                                isSuccess = true;
                            }; break;
                        case "organizationalUnit":
                            {
                                DirectoryEntry oOU = GetDirectoryObjectforOU(objects, domain);
                                oOU.Rename("OU=" + newobjects);
                                oOU.CommitChanges();
                                oOU.Close();
                                isSuccess = true;
                            }; break;
                        case "computer":
                            {
                                DirectoryEntry ocomputer = GetDirectoryEntryOfComputer(objects, domain).GetDirectoryEntry();
                                ocomputer.Properties["sAMAccountName"][0] = (newobjects.ToUpper() + "$");
                                ocomputer.CommitChanges();
                                ocomputer.Rename("cn=" + newobjects);
                                ocomputer.CommitChanges();
                                ocomputer.Close();
                                isSuccess = true;
                            }; break;// 判断计算机是否存在
                        case "wWWHomePage":
                            {
                                DirectoryEntry job = GetDirectoryEntryByJobnumber(objects, domain).GetDirectoryEntry();
                                job.Properties["sAMAccountName"][0] = newobjects;
                                job.CommitChanges();
                                job.Properties["userPrincipalName"][0] = (newobjects + sel["fulldomain"]);
                                job.CommitChanges();
                                job.Rename("cn=" + newobjects);
                                job.CommitChanges();
                                job.Close();
                                isSuccess = true;
                            }; break;

                        default: isSuccess = false; ; break;
                    }

                    var message = new { message = "更名为：" + newobjects };
                    var result = new { isSuccess = isSuccess, message = message };
                    HttpResponseMessage resultjson = toJson(result);
                    return resultjson;
                }
                catch (Exception ex)
                {
                    var message = new { message = ex.Message };
                    var result = new { isSuccess = isSuccess, message = message };
                    HttpResponseMessage resultjson = toJson(result);
                    return resultjson;
                }
            }
            else
            {
                var message = new { message = "API没经过授权无法调用!!!" };
                var result = new { isSuccess = isSuccess, message = message };
                HttpResponseMessage resultjson = toJson(result);
                return resultjson;
            }
        }

        #endregion

        #region （21）user开通邮箱
        [HttpGet]
        public HttpResponseMessage UserToExc(string username, string dbname, string skey, string domain)
        {

            try
            {
                var message = string.Empty;
                var isSuccess = false;
                if (skey == admd5(domain))
                {
                    Thread.Sleep(25000);

                    var connInfo = mailexloginin(domain);
                    var runspace = RunspaceFactory.CreateRunspace(connInfo);
                    var command = new Command("Enable-Mailbox");
                    command.Parameters.Add("Identity", username);
                    command.Parameters.Add("Alias", username);
                    command.Parameters.Add("Database", dbname);
                    runspace.Open();
                    var pipeline = runspace.CreatePipeline();
                    pipeline.Commands.Add(command);
                    var results = pipeline.Invoke();
                    runspace.Dispose();
                    message += username + "邮箱开通成功。";
                    isSuccess = true;
                }
                else
                {
                    message = "API没经过授权无法调用!!!";
                }
                var result = new { isSuccess = isSuccess, message = message };
                HttpResponseMessage resultjson = toJson(result);
                return resultjson;
            }
            catch (Exception ex)
            {
                var message = new { message = ex.Message };
                var result = new { isSuccess = false, message = message };
                HttpResponseMessage resultjson = toJson(result);
                return resultjson;
            }
        }
        #endregion

        #region （22）user创建邮箱归档
        [HttpGet]
        public HttpResponseMessage CreateMailboxArchive(string username, string skey, string domain)
        {
            var isSuccess = false;
            if (skey == admd5(domain))
            {

                try
                {
                    if (username == string.Empty || username == null)
                    {
                        var message = new { message = username + "不能为空" };
                        var result = new { isSuccess = isSuccess, message = message };
                        HttpResponseMessage resultjson = toJson(result);
                        return resultjson;
                    }
                    else
                    {
                        //Thread.Sleep(60000);
                        Mysqldbinfo dbinfo = new Mysqldbinfo();
                        Dictionary<string, string> selmail = dbinfo.SelMailConfig(domain);
                        DirectoryEntry deuser = GetDirectoryEntryOfUser(username, domain).GetDirectoryEntry();
                        deuser.Properties["msExchArchiveDatabaseLink"].Value = selmail["msExchArchiveDatabaseLink"];//归档邮箱数据库
                        deuser.Properties["msExchArchiveGUID"].Value = Guid.NewGuid().ToByteArray(); //归档邮箱GUID
                        deuser.Properties["msExchArchiveName"].Value = selmail["msExchArchiveName"] + deuser.Properties["displayName"].Value; //归档邮箱名称
                        deuser.Properties["msExchArchiveQuota"].Value = selmail["msExchArchiveQuota"]; //归档邮箱配额大小
                        deuser.CommitChanges();
                        deuser.Properties["msExchArchiveWarnQuota"].Value = selmail["msExchArchiveWarnQuota"]; //归档邮箱报警提示配额
                        deuser.Properties["msExchELCMailboxFlags"].Value = selmail["msExchELCMailboxFlags"];
                        deuser.Properties["msExchMailboxTemplateLink"].Value = selmail["msExchMailboxTemplateLink"];
                        deuser.CommitChanges();
                        deuser.Close();
                        var message = new { message = selmail["msExchArchiveName"] + deuser.Properties["displayName"].Value + "创建成功" };
                        var result = new { isSuccess = true, message = message };
                        HttpResponseMessage resultjson = toJson(result);
                        return resultjson;
                    }
                }
                catch (Exception ex)
                {
                    var message = new { message = ex.Message };
                    var result = new { isSuccess = isSuccess, message = message };
                    HttpResponseMessage resultjson = toJson(result);
                    return resultjson;
                }
            }
            else
            {
                var message = new { message = "API没经过授权无法调用!!!" };
                var result = new { isSuccess = isSuccess, message = message };
                HttpResponseMessage resultjson = toJson(result);
                return resultjson;
            }
        }
        #endregion

        #region (23)新增用户smtp地址
        /// <summary>
        ///  新增用户smtp地址
        /// </summary>
        /// <param name="username">用户名</param>
        /// <param name="smtpValue">smtp地址</param>
        [HttpGet]
        public HttpResponseMessage setuseremailadress(string username, string smtpValue, string skey, string domain)
        {
            var isSuccess = false;
            if (skey == admd5(domain))
            {
                if (smtpValue != null)
                {
                    try
                    {
                        if (ObjectExists(username, "user", domain))
                        {
                            DirectoryEntry oUser = GetDirectoryEntryOfUser(username, domain).GetDirectoryEntry();
                            oUser.Properties["proxyAddresses"].Add("smtp:" + smtpValue);
                            oUser.CommitChanges();
                            oUser.Close();
                            isSuccess = true;
                            var message = new { message = username + "的smtp地址添加成功" };
                            var result = new { isSuccess = isSuccess, message = message };
                            HttpResponseMessage resultjson = toJson(result);
                            return resultjson;
                        }
                        else
                        {
                            var message = new { message = username + "，在AD中不存在。" };
                            var result = new { isSuccess = isSuccess, message = message };
                            HttpResponseMessage resultjson = toJson(result);
                            return resultjson;
                        }
                    }
                    catch (Exception ex)
                    {
                        var message = new { message = ex.Message };
                        var result = new { isSuccess = isSuccess, message = message };
                        HttpResponseMessage resultjson = toJson(result);
                        return resultjson;
                    }
                }
                else
                {
                    var message = new { message = smtpValue + "不能为空" };
                    var result = new { isSuccess = isSuccess, message = message };
                    HttpResponseMessage resultjson = toJson(result);
                    return resultjson;
                }
            }
            else
            {
                var message = new { message = "API没经过授权无法调用!!!" };
                var result = new { isSuccess = isSuccess, message = message };
                HttpResponseMessage resultjson = toJson(result);
                return resultjson;
            }
        }

        #endregion

        #region (24)删除用户smtp地址
        /// <summary>
        ///  删除用户smtp地址
        /// </summary>
        /// <param name="username">用户名</param>
        /// <param name="smtpValue">smtp地址</param>
        [HttpGet]
        public HttpResponseMessage deluseremailadress(string username, string smtpValue, string skey, string domain)
        {
            var isSuccess = false;
            if (skey == admd5(domain))
            {
                if (smtpValue != null)
                {
                    try
                    {
                        if (ObjectExists(username, "user", domain))
                        {
                            DirectoryEntry oUser = GetDirectoryEntryOfUser(username, domain).GetDirectoryEntry();
                            oUser.Properties["proxyAddresses"].Remove("smtp:" + smtpValue);
                            oUser.CommitChanges();
                            oUser.Close();
                            isSuccess = true;
                            var message = new { message = username + "的smtp地址添加成功" };
                            var result = new { isSuccess = isSuccess, message = message };
                            HttpResponseMessage resultjson = toJson(result);
                            return resultjson;
                        }
                        else
                        {
                            var message = new { message = username + "，在AD中不存在。" };
                            var result = new { isSuccess = isSuccess, message = message };
                            HttpResponseMessage resultjson = toJson(result);
                            return resultjson;
                        }
                    }
                    catch (Exception ex)
                    {
                        var message = new { message = ex.Message };
                        var result = new { isSuccess = isSuccess, message = message };
                        HttpResponseMessage resultjson = toJson(result);
                        return resultjson;
                    }
                }
                else
                {
                    var message = new { message = smtpValue + "不能为空" };
                    var result = new { isSuccess = isSuccess, message = message };
                    HttpResponseMessage resultjson = toJson(result);
                    return resultjson;
                }
            }
            else
            {
                var message = new { message = "API没经过授权无法调用!!!" };
                var result = new { isSuccess = isSuccess, message = message };
                HttpResponseMessage resultjson = toJson(result);
                return resultjson;
            }
        }

        #endregion

        #region (25)New-MoveRequestArchive迁移用户邮箱和存档数据库
        /// <summary>
        /// New-MoveRequest
        ///  迁移用户邮箱数据库
        /// </summary>
        /// <param name="Identity">用户名</param>
        /// <param name="TargetDatabase">用户新数据库地址</param>
        /// /// <param name="ArchiveTargetDatabase">存档新数据库地址</param>
        [HttpGet]
        public HttpResponseMessage NewMoveRequestArchive(string username, string TargetDatabase, string ArchiveTargetDatabase, string skey, string domain)
        {
            try
            {
                var message = string.Empty;
                var isSuccess = false;
                if (skey == admd5(domain))
                {

                    var connInfo = mailexloginin(domain);
                    var runspace = RunspaceFactory.CreateRunspace(connInfo);
                    var command = new Command("New-MoveRequest");
                    command.Parameters.Add("Identity", username);
                    command.Parameters.Add("TargetDatabase", TargetDatabase);
                    command.Parameters.Add("ArchiveTargetDatabase", ArchiveTargetDatabase);
                    command.Parameters.Add("Confirm", Convert.ToBoolean("false"));
                    runspace.Open();
                    var pipeline = runspace.CreatePipeline();
                    pipeline.Commands.Add(command);
                    var results = pipeline.Invoke();
                    runspace.Dispose();
                    if (results.Count.ToString() != "1")
                    {
                        message += "执行错误";
                    }
                    else
                    {
                        isSuccess = true;
                        message = "已接收移动请求！";
                    }
                }
                else
                {
                    message = "API没经过授权无法调用!!!";
                }
                var result = new { isSuccess = isSuccess, message = message };
                HttpResponseMessage resultjson = toJson(result);
                return resultjson;
            }
            catch (Exception ex)
            {
                var message = new { message = ex.Message };
                var result = new { isSuccess = false, message = message };
                HttpResponseMessage resultjson = toJson(result);
                return resultjson;
            }
        }

        #endregion

        #region (26)修改邮箱
        [HttpGet]
        public HttpResponseMessage EditMail(string username, string skey, string domain)
        {
            var isSuccess = false;
            if (skey == admd5(domain))
            {
                if (username != null)
                {
                    try
                    {
                        if (ObjectExists(username, "user", domain))
                        {
                            Mysqldbinfo dbinfo = new Mysqldbinfo();
                            var sel = dbinfo.Selglobals(domain);
                            DirectoryEntry deuser = GetDirectoryEntryOfUser(username, domain).GetDirectoryEntry();
                            //移除老的地址
                            deuser.Properties["proxyAddresses"].Clear();
                            deuser.Properties["mailNickName"].Clear();
                            deuser.CommitChanges();
                            deuser.Properties["legacyExchangeDN"].Value = "/o=First Organization/ou=Exchange Administrative Group (FYDIBOHF23SPDLT)/cn=Recipients/cn=" + username;//调用时 需要添加邮箱前缀
                            deuser.Properties["mailNickName"].Add(username);
                            deuser.Properties["proxyAddresses"].Add("smtp:" + username + sel["fulldomain"]);
                            deuser.CommitChanges();
                            deuser.Close();
                            isSuccess = true;
                            var message = new { message = username + "的邮箱修改成功" };
                            var result = new { isSuccess = isSuccess, message = message };
                            HttpResponseMessage resultjson = toJson(result);
                            return resultjson;
                        }
                        else
                        {
                            var message = new { message = username + "，在AD中不存在。" };
                            var result = new { isSuccess = isSuccess, message = message };
                            HttpResponseMessage resultjson = toJson(result);
                            return resultjson;
                        }
                    }
                    catch (Exception ex)
                    {
                        var message = new { message = ex.Message };
                        var result = new { isSuccess = isSuccess, message = message };
                        HttpResponseMessage resultjson = toJson(result);
                        return resultjson;
                    }
                }
                else
                {
                    var message = new { message = username + "不能为空" };
                    var result = new { isSuccess = isSuccess, message = message };
                    HttpResponseMessage resultjson = toJson(result);
                    return resultjson;
                }
            }
            else
            {
                var message = new { message = "API没经过授权无法调用!!!" };
                var result = new { isSuccess = isSuccess, message = message };
                HttpResponseMessage resultjson = toJson(result);
                return resultjson;
            }
        }

        #endregion

        #region (27)根据对象类别修改用户属性
        [HttpGet]
        public HttpResponseMessage SetobjectProperty(string objects, string objectClass, string PropertyName, string PropertyValue, string skey, string domain)
        {
            var isSuccess = false;
            if (skey == admd5(domain))
            {
                if (PropertyValue != null)
                {
                    try
                    {

                        switch (objectClass)
                        {
                            case "user":
                                {
                                    DirectoryEntry oUser = GetDirectoryEntryOfUser(objects, domain).GetDirectoryEntry();
                                    if (oUser.Properties.Contains(PropertyName))
                                    {
                                        oUser.Properties[PropertyName][0] = PropertyValue;
                                    }
                                    else
                                    {
                                        oUser.Properties[PropertyName].Add(PropertyValue);
                                    }
                                    oUser.CommitChanges();
                                    oUser.Close();
                                    isSuccess = true;
                                }; break;

                            case "group":
                                {
                                    DirectoryEntry oUser = GetDirectoryEntryOfGroup(objects, domain).GetDirectoryEntry();
                                    if (oUser.Properties.Contains(PropertyName))
                                    {
                                        oUser.Properties[PropertyName][0] = PropertyValue;
                                    }
                                    else
                                    {
                                        oUser.Properties[PropertyName].Add(PropertyValue);
                                    }
                                    oUser.CommitChanges();
                                    oUser.Close();
                                    isSuccess = true;
                                }; break;
                            case "organizationalUnit":
                                {
                                    DirectoryEntry oUser = GetDirectoryobject(objects, domain);
                                    if (oUser.Properties.Contains(PropertyName))
                                    {
                                        oUser.Properties[PropertyName][0] = PropertyValue;
                                    }
                                    else
                                    {
                                        oUser.Properties[PropertyName].Add(PropertyValue);
                                    }
                                    oUser.CommitChanges();
                                    oUser.Close();
                                    isSuccess = true;
                                }; break;
                            case "computer":
                                {
                                    DirectoryEntry oUser = GetDirectoryEntryOfComputer(objects, domain).GetDirectoryEntry();
                                    if (oUser.Properties.Contains(PropertyName))
                                    {
                                        oUser.Properties[PropertyName][0] = PropertyValue;
                                    }
                                    else
                                    {
                                        oUser.Properties[PropertyName].Add(PropertyValue);
                                    }
                                    oUser.CommitChanges();
                                    oUser.Close();
                                    isSuccess = true;
                                }; break;// 判断计算机是否存在
                            case "jobnumber":
                                {
                                    DirectoryEntry oUser = GetDirectoryEntryByJobnumber(objects, domain).GetDirectoryEntry();
                                    if (oUser.Properties.Contains(PropertyName))
                                    {
                                        oUser.Properties[PropertyName][0] = PropertyValue;
                                    }
                                    else
                                    {
                                        oUser.Properties[PropertyName].Add(PropertyValue);
                                    }
                                    oUser.CommitChanges();
                                    oUser.Close();
                                    isSuccess = true;
                                }; break;

                            default: isSuccess = false; ; break;
                        }

                        var message = new { message = objects + "的" + PropertyName + "属性，修改成功" };
                        var result = new { isSuccess = isSuccess, message = message };
                        HttpResponseMessage resultjson = toJson(result);
                        return resultjson;

                    }
                    catch (Exception ex)
                    {
                        var message = new { message = ex.Message };
                        var result = new { isSuccess = isSuccess, message = message };
                        HttpResponseMessage resultjson = toJson(result);
                        return resultjson;
                    }
                }
                else
                {
                    var message = new { message = PropertyValue + "不能为空" };
                    var result = new { isSuccess = isSuccess, message = message };
                    HttpResponseMessage resultjson = toJson(result);
                    return resultjson;
                }
            }
            else
            {
                var message = new { message = "API没经过授权无法调用!!!" };
                var result = new { isSuccess = isSuccess, message = message };
                HttpResponseMessage resultjson = toJson(result);
                return resultjson;
            }
        }
        #endregion

        #region （28）get-mailboxdatabase-novalue
        /// <summary>
        /// 远程执行get-mailboxdatabase命令
        /// 获取所有邮箱数据库信息
        /// </summary>
        /// <param name="skey"></param>
        /// <returns></returns>
        [HttpGet]
        public HttpResponseMessage getmailboxdatabasenovalue(string skey, string domain)
        {
            try
            {
                List<string> message = new List<string>();
                var isSuccess = false;
                if (skey == admd5(domain))
                {

                    var connInfo = mailexloginin(domain);
                    var runspace = RunspaceFactory.CreateRunspace(connInfo);
                    var command = new Command("get-mailboxdatabase");
                    //command.Parameters.Add("Alias", sGroup);
                    runspace.Open();
                    var pipeline = runspace.CreatePipeline();
                    pipeline.Commands.Add(command);
                    var results = pipeline.Invoke();
                    runspace.Dispose();
                    if (results.Count.ToString() == "0")
                    {
                        message.Add("无邮箱数据库");
                    }
                    else
                    {
                        for (int i = 0; i < int.Parse(results.Count.ToString()); i++)
                        {
                            try
                            {
                                message.Add("{'daname':'" + results[i].Members["name"].Value + "'}");
                                isSuccess = true;
                            }
                            catch (Exception)
                            {
                                message.Add("权限不存在");
                                var result1 = new { isSuccess = isSuccess, message = message };
                                HttpResponseMessage resultjson1 = toJson(result1);
                                return resultjson1;
                            }
                        }
                    }
                }
                else
                {
                    message.Add("API没经过授权无法调用!!!");
                }
                var result = new { isSuccess = isSuccess, message = message };
                HttpResponseMessage resultjson = toJson(result);
                return resultjson;
            }
            catch (Exception ex)
            {
                var message = new { message = ex.Message };
                var result = new { isSuccess = false, message = message };
                HttpResponseMessage resultjson = toJson(result);
                return resultjson;
            }
        }
        #endregion

        #region (29)删除AD账号
        /// <summary>
        ///  删除AD账号
        /// </summary>
        /// <param name="username">用户名</param>
        [HttpGet]
        public HttpResponseMessage delaccount(string username, string skey, string domain)
        {
            var isSuccess = false;
            if (skey == admd5(domain))
            {

                try
                {
                    if (ObjectExists(username, "user", domain))
                    {
                        DirectoryEntry oUser = GetDirectoryEntryOfUser(username, domain).GetDirectoryEntry();
                        oUser.DeleteTree();
                        oUser.Close();
                        isSuccess = true;
                        var message = new { message = username + ",在AD中删除成功" };
                        var result = new { isSuccess = isSuccess, message = message };
                        HttpResponseMessage resultjson = toJson(result);
                        return resultjson;
                    }
                    else
                    {
                        var message = new { message = username + "，在AD中不存在。" };
                        var result = new { isSuccess = isSuccess, message = message };
                        HttpResponseMessage resultjson = toJson(result);
                        return resultjson;
                    }
                }
                catch (Exception ex)
                {
                    var message = new { message = ex.Message };
                    var result = new { isSuccess = isSuccess, message = message };
                    HttpResponseMessage resultjson = toJson(result);
                    return resultjson;
                }

            }
            else
            {
                var message = new { message = "API没经过授权无法调用!!!" };
                var result = new { isSuccess = isSuccess, message = message };
                HttpResponseMessage resultjson = toJson(result);
                return resultjson;
            }
        }

        #endregion

        #region (30)Set-Mailbox 通讯簿
        /// <summary>
        /// Set-Mailbox
        ///  这个账号是否显示在Exchange通讯簿上
        /// </summary>
        /// <param name="Identity">用户名</param>

        [HttpGet]
        public HttpResponseMessage ListsEnabled(string username, string isaddressbook, string skey, string domain)
        {
            var message = string.Empty;
            var isSuccess = false;
            if (skey == admd5(domain))
            {

                var connInfo = mailexloginin(domain);
                var runspace = RunspaceFactory.CreateRunspace(connInfo);
                var command = new Command("Set-Mailbox");
                command.Parameters.Add("Identity", username);
                if (isaddressbook == "1")
                {
                    command.Parameters.Add("HiddenFromAddressListsEnabled", Convert.ToBoolean("true"));
                }
                else
                {
                    command.Parameters.Add("HiddenFromAddressListsEnabled", Convert.ToBoolean("false"));
                }
                runspace.Open();
                var pipeline = runspace.CreatePipeline();
                pipeline.Commands.Add(command);
                var results = pipeline.Invoke();
                runspace.Dispose();
                if (results.Count.ToString() == "0")
                {
                    isSuccess = true;
                    message = "修改通讯簿选项成功";
                }
                else
                {
                    message += "执行错误";
                }
            }
            else
            {
                message = "API没经过授权无法调用!!!";
            }
            var result = new { isSuccess = isSuccess, message = message };
            HttpResponseMessage resultjson = toJson(result);
            return resultjson;
        }

        #endregion

        #region （31）根据cn获取组信息
        /// <summary>
        /// 根据cn获取组信息
        /// </summary>
        /// <param name="skey"></param>
        /// <returns></returns>
        [HttpGet]
        public HttpResponseMessage Showgroupname(string groupname, string skey, string domain)
        {
            var isSuccess = false;
            if (skey == admd5(domain))
            {
                try
                {
                    DirectoryEntry oUser = GetDirectoryEntryOfGroup(groupname, domain).GetDirectoryEntry();
                    oUser.CommitChanges();
                    var aduser =
                    new
                    {
                        cn = oUser.Properties["cn"].Value,
                        name = oUser.Properties["name"].Value,
                        sAMAccountName = oUser.Properties["sAMAccountName"].Value,//账户登陆名(Windows 2000 以前版本)
                        displayname = oUser.Properties["displayName"].Value, //显示名称
                        description = oUser.Properties["description"].Value, //描述
                        managedBy = oUser.Properties["managedBy"].Value, //描述
                        mail = oUser.Properties["mail"].Value, // 邮箱号
                        whenCreated = oUser.Properties["whenCreated"].Value.ToString(), // 用户创建时间
                        whenChanged = oUser.Properties["whenChanged"].Value.ToString(), // 更新用户时间
                        memberof = oUser.Properties["memberof"].Value, //用户权限
                        member = oUser.Properties["member"].Value, //用户权限

                    };
                    oUser.Close();
                    isSuccess = true;
                    var result = new { isSuccess = isSuccess, message = aduser };
                    HttpResponseMessage resultjson = toJson(result);
                    return resultjson;

                }
                catch (Exception ex)
                {
                    var message = new { message = ex.Message };
                    var result = new { isSuccess = isSuccess, message = message };
                    HttpResponseMessage resultjson = toJson(result);
                    return resultjson;
                }
            }
            else
            {
                var message = new { message = "API没经过授权无法调用!!!" };
                var result = new { isSuccess = isSuccess, message = message };
                HttpResponseMessage resultjson = toJson(result);
                return resultjson;
            }

        }
        #endregion

        #region （31.1）根据samaccountname删除组
        /// <summary>
        /// 根据cn获取组信息
        /// </summary>
        /// <param name="skey"></param>
        /// <returns></returns>
        [HttpGet]
        public HttpResponseMessage delgroupbyname(string groupname, string skey, string domain)
        {
            var isSuccess = false;
            if (skey == admd5(domain))
            {
                try
                {
                    DirectoryEntry oGroup = GetDirectoryEntryOfGroup(groupname, domain).GetDirectoryEntry();
                    oGroup.DeleteTree();
                    oGroup.Close();
                    isSuccess = true;
                    var result = new { isSuccess = isSuccess, message = "删除成功" };
                    HttpResponseMessage resultjson = toJson(result);
                    return resultjson;
                }
                catch (Exception ex)
                {
                    var result = new { isSuccess = isSuccess, message = ex.Message };
                    HttpResponseMessage resultjson = toJson(result);
                    return resultjson;
                }
            }
            else
            {
                var message = new { message = "API没经过授权无法调用!!!" };
                var result = new { isSuccess = isSuccess, message = message };
                HttpResponseMessage resultjson = toJson(result);
                return resultjson;
            }

        }
        #endregion


        #region （31.5）根据managedBy获取组信息
        /// <summary>
        /// 根据cn获取组信息
        /// </summary>
        /// <param name="skey"></param>
        /// <returns></returns>
        [HttpGet]
        public HttpResponseMessage ShowgroupnamebymanagedBy(string managedBy, string skey, string domain)
        {
            var isSuccess = false;
            if (skey == admd5(domain))
            {
                try
                {
                    SearchResultCollection oUser = GetDirectoryEntryOfmanagedBy(managedBy, domain);                    
                    isSuccess = true;
                    var result = new { isSuccess = isSuccess, message = oUser };
                    HttpResponseMessage resultjson = toJson(result);
                    return resultjson;

                }
                catch (Exception ex)
                {
                    var message = new { message = ex.Message };
                    var result = new { isSuccess = isSuccess, message = message };
                    HttpResponseMessage resultjson = toJson(result);
                    return resultjson;
                }
            }
            else
            {
                var message = new { message = "API没经过授权无法调用!!!" };
                var result = new { isSuccess = isSuccess, message = message };
                HttpResponseMessage resultjson = toJson(result);
                return resultjson;
            }

        }
        #endregion

        #region （32）Get-DistributionGroup
        /// <summary>
        /// 远程执行Get-DistributionGroup命令
        /// 一般用作获取邮箱群组发件人限制属性
        /// </summary>
        /// <param name="skey"></param>
        /// <returns></returns>
        [HttpGet]
        public HttpResponseMessage GetDistributionGroup(string pyname, string pyvalue, string skey, string domain)
        {
            try
            {
                List<string> message = new List<string>();
                var isSuccess = false;
                if (skey == admd5(domain))
                {

                    var connInfo = mailexloginin(domain);
                    var runspace = RunspaceFactory.CreateRunspace(connInfo);
                    var command = new Command("Get-DistributionGroup");
                    command.Parameters.Add("Identity", pyname);
                    runspace.Open();
                    var pipeline = runspace.CreatePipeline();
                    pipeline.Commands.Add(command);
                    var results = pipeline.Invoke();
                    runspace.Dispose();
                    if (results.Count.ToString() == "0")
                    {
                        message.Add("找不到用户");
                    }
                    else
                    {
                        for (int i = 0; i < int.Parse(results.Count.ToString()); i++)
                        {
                            try
                            {
                                message.Add("{'daname':'" + results[i].Members[pyvalue].Value + "'}");
                                isSuccess = true;
                            }
                            catch (Exception)
                            {
                                message.Add("权限不存在");
                                var result1 = new { isSuccess = isSuccess, message = message };
                                HttpResponseMessage resultjson1 = toJson(result1);
                                return resultjson1;
                            }
                        }
                    }
                }
                else
                {
                    message.Add("API没经过授权无法调用!!!");
                }
                var result = new { isSuccess = isSuccess, message = message };
                HttpResponseMessage resultjson = toJson(result);
                return resultjson;
            }
            catch (Exception ex)
            {
                var message = new { message = ex.Message };
                var result = new { isSuccess = false, message = message };
                HttpResponseMessage resultjson = toJson(result);
                return resultjson;
            }
        }
        #endregion

        #region （32.1）Get-DistributionGroup
        /// <summary>
        /// 远程执行Get-DistributionGroup命令
        /// 一般用作获取邮箱群组发件人限制属性
        /// </summary>
        /// <param name="skey"></param>
        /// <returns></returns>
        [HttpGet]
        public HttpResponseMessage GetDistributionGroupSendto(string pyname, string pyvalue, string skey, string domain)
        {
            try
            {
                List<string> message = new List<string>();
                var isSuccess = false;
                if (skey == admd5(domain))
                {

                    var connInfo = mailexloginin(domain);
                    var runspace = RunspaceFactory.CreateRunspace(connInfo);
                    var command = new Command("Get-DistributionGroup");
                    command.Parameters.Add("Identity", pyname);
                    runspace.Open();
                    var pipeline = runspace.CreatePipeline();
                    pipeline.Commands.Add(command);
                    var results = pipeline.Invoke();
                    runspace.Dispose();
                    if (results.Count.ToString() == "0")
                    {
                        message.Add("找不到用户");
                    }
                    else
                    {
                        try
                        {
                            List<object> gggg = new List<object>();
                            message.Add("{'daname':'" + results[0].Members[pyvalue].Value + "'}");
                            var firstvalue = results[0].Members[pyvalue].Value as PSObject;
                            ArrayList listvalue = firstvalue.BaseObject as ArrayList;
                            foreach (object oonvalue in listvalue)
                            {
                                gggg.Add(oonvalue);
                            }
                            isSuccess = true;

                            var result1 = new { isSuccess = isSuccess, message = gggg };
                            HttpResponseMessage resultjson1 = toJson(result1);
                            return resultjson1;
                        }
                        catch (Exception)
                        {
                            message.Add("权限不存在");
                            var result1 = new { isSuccess = isSuccess, message = message };
                            HttpResponseMessage resultjson1 = toJson(result1);
                            return resultjson1;
                        }
                    }

                }
                else
                {
                    message.Add("API没经过授权无法调用!!!");
                }
                var result = new { isSuccess = isSuccess, message = message };
                HttpResponseMessage resultjson = toJson(result);
                return resultjson;
            }
            catch (Exception ex)
            {
                var message = new { message = ex.Message };
                var result = new { isSuccess = false, message = message };
                HttpResponseMessage resultjson = toJson(result);
                return resultjson;
            }
        }
        #endregion


        #region （32.2）Get-DistributionGroup
        /// <summary>
        /// 远程执行Get-DistributionGroup命令
        /// 一般用作获取邮箱群组发件人限制属性
        /// </summary>
        /// <param name="skey"></param>
        /// <returns></returns>
        [HttpGet]
        public HttpResponseMessage GetDistributionGroupselect(string pyname, string skey, string domain)
        {
            try
            {
                List<object> message = new List<object>();
                var isSuccess = false;
                if (skey == admd5(domain))
                {

                    var connInfo = mailexloginin(domain);
                    var runspace = RunspaceFactory.CreateRunspace(connInfo);
                    var command = new Command("Get-DistributionGroup");
                    command.Parameters.Add("Identity", pyname);
                    runspace.Open();
                    var pipeline = runspace.CreatePipeline();
                    pipeline.Commands.Add(command);
                    var results = pipeline.Invoke();
                    runspace.Dispose();
                    if (results.Count.ToString() == "0")
                    {
                        message.Add("找不到用户");
                    }
                    else
                    {
                            try
                            {
                            var aaa = new { DisplayName = results[0].Members["DisplayName"].Value, SamAccountName = results[0].Members["SamAccountName"].Value, PrimarySmtpAddress = results[0].Members["PrimarySmtpAddress"].Value, };
                            message.Add(aaa);
                            isSuccess = true;
                            var result1 = new { isSuccess = isSuccess, message = message };
                            HttpResponseMessage resultjson1 = toJson(result1);
                            return resultjson1;
                        }
                            catch (Exception)
                            {
                                message.Add("权限不存在");
                                var result1 = new { isSuccess = isSuccess, message = message };
                                HttpResponseMessage resultjson1 = toJson(result1);
                                return resultjson1;
                            }
                        
                    }
                }
                else
                {
                    message.Add("API没经过授权无法调用!!!");
                }
                var result = new { isSuccess = isSuccess, message = message };
                HttpResponseMessage resultjson = toJson(result);
                return resultjson;
            }
            catch (Exception ex)
            {
                var message = new { message = ex.Message };
                var result = new { isSuccess = false, message = message };
                HttpResponseMessage resultjson = toJson(result);
                return resultjson;
            }
        }
        #endregion

        #region （33）set-DistributionGroup
        /// <summary>
        /// 远程执行set-DistributionGroup命令
        /// 一般用作设置邮箱群组发件人限制属性
        /// </summary>
        /// <param name="skey"></param>
        /// <returns></returns>
        [HttpGet]
        public HttpResponseMessage SetDistributionGroup(string Identity ,string pyname, string pyvalue, string skey, string domain)
        {
            List<string> message = new List<string>();
            try
            {
                var isSuccess = false;
                if (skey == admd5(domain))
                {

                    var connInfo = mailexloginin(domain);
                    var runspace = RunspaceFactory.CreateRunspace(connInfo);
                    var command = new Command("Set-DistributionGroup");
                    command.Parameters.Add("Identity", Identity);
                    command.Parameters.Add(pyname, pyvalue);
                    runspace.Open();
                    var pipeline = runspace.CreatePipeline();
                    pipeline.Commands.Add(command);
                    pipeline.Invoke();
                    runspace.Dispose();
                    isSuccess = true;
                    message.Add("");
                }
                else
                {
                    message.Add("API没经过授权无法调用!!!");
                }
                var result = new { isSuccess = isSuccess, message = message };
                HttpResponseMessage resultjson = toJson(result);
                return resultjson;
            }
            catch (Exception ex)
            {
                message.Add(ex.Message);
                var result = new { isSuccess = false, message = message };
                HttpResponseMessage resultjson = toJson(result);
                return resultjson;
            }
        }
        #endregion

        #region （33.1）set-DistributionGroup  bool
        /// <summary>
        /// 远程执行set-DistributionGroup命令
        /// 一般用作设置邮箱群组发件人限制属性
        /// </summary>
        /// <param name="skey"></param>
        /// <returns></returns>
        [HttpGet]
        public HttpResponseMessage SetDistributionGroupbybool(string Identity, string pyname, string pyvalue, string skey, string domain)
        {
            List<string> message = new List<string>();
            try
            {
                var isSuccess = false;
                if (skey == admd5(domain))
                {

                    var connInfo = mailexloginin(domain);
                    var runspace = RunspaceFactory.CreateRunspace(connInfo);
                    var command = new Command("Set-DistributionGroup");
                    command.Parameters.Add("Identity", Identity);
                    command.Parameters.Add(pyname, Convert.ToBoolean(pyvalue));
                    runspace.Open();
                    var pipeline = runspace.CreatePipeline();
                    pipeline.Commands.Add(command);
                    pipeline.Invoke();
                    runspace.Dispose();
                    isSuccess = true;
                    message.Add("");
                }
                else
                {
                    message.Add("API没经过授权无法调用!!!");
                }
                var result = new { isSuccess = isSuccess, message = message };
                HttpResponseMessage resultjson = toJson(result);
                return resultjson;
            }
            catch (Exception ex)
            {
                message.Add(ex.Message);
                var result = new { isSuccess = false, message = message };
                HttpResponseMessage resultjson = toJson(result);
                return resultjson;
            }
        }
        #endregion


        #region (34)根据用户smstp查询属性
        [HttpGet]
        public HttpResponseMessage GetobjectPropertybysmtp(string objects, string skey, string domain)
        {
            var isSuccess = false;
            if (skey == admd5(domain))
            {
                try
                {

                    ArrayList mList = new ArrayList();
                    DirectoryEntry oUser = GetDirectoryEntryOfUserBySmtp(objects, domain).GetDirectoryEntry();
                    oUser.CommitChanges();
                    var pwdset = GetDateTimeFromLargeInteger((IADsLargeInteger)oUser.Properties["pwdLastSet"].Value).ToString();//system.__comobject 先转换成IADsLargeInteger再转换成datatime
                    string PasswordExpirationDate = oUser.InvokeGet("PasswordExpirationDate").ToString(); //获取密码到期时间
                    if (PasswordExpirationDate == "1970/1/1 0:00:00")
                    {
                        PasswordExpirationDate = "密码永不过期";
                    }
                    var aduser =
                    new
                    {
                        cn = oUser.Properties["cn"].Value,
                        name = oUser.Properties["name"].Value,
                        sn = oUser.Properties["sn"].Value,//姓(L)
                        givenName = oUser.Properties["givenName"].Value,//名(F)
                        sAMAccountName = oUser.Properties["sAMAccountName"].Value,//账户登陆名(Windows 2000 以前版本)
                        userPrincipalName = oUser.Properties["userPrincipalName"].Value,//账户登陆
                        displayName = oUser.Properties["displayName"].Value, //显示名称
                        wWWHomePage = oUser.Properties["wWWHomePage"].Value, //工号
                        guid = oUser.Properties["physicalDeliveryOfficeName"].Value,//办公室(C)   
                        description = oUser.Properties["description"].Value, //描述
                        mail = oUser.Properties["mail"].Value, // 邮箱号
                        distinguishedName = oUser.Properties["distinguishedName"].Value, // 位置
                        homeMDB = oUser.Properties["homeMDB"].Value, // 用户邮箱号数据
                        PasswordExpirationDate = PasswordExpirationDate, // 密码到期时间
                        pwdLastSet = pwdset,//上次修改密码时间
                        whenCreated = oUser.Properties["whenCreated"].Value.ToString(), // 用户创建时间
                        whenChanged = oUser.Properties["whenChanged"].Value.ToString(), // 更新用户时间
                        memberof = oUser.Properties["memberof"].Value, //用户权限
                        proxyAddresses = oUser.Properties["proxyAddresses"].Value,//smtp
                        userAccountControl = oUser.Properties["userAccountControl"].Value,//启用。禁用
                        IsAccountLocked = userlock(objects, domain),  //0没有锁定，其他被锁定
                    };
                    oUser.Close();
                    mList.Add(aduser);
                    isSuccess = true;
                    var result = new { isSuccess = isSuccess, message = mList };
                    HttpResponseMessage resultjson = toJson(result);
                    return resultjson;
                }
                catch (Exception ex)
                {
                    var message = new { message = ex.Message };
                    var result = new { isSuccess = isSuccess, message = message };
                    HttpResponseMessage resultjson = toJson(result);
                    return resultjson;
                }
            }
            else
            {
                var message = new { message = "API没经过授权无法调用!!!" };
                var result = new { isSuccess = isSuccess, message = message };
                HttpResponseMessage resultjson = toJson(result);
                return resultjson;
            }
        }
        #endregion

        #region （41.1）Set-Mailbox
        /// <summary>
        /// 远程执行Set-Mailbox命令
        /// 修改用户邮箱容量数据库等信息
        /// </summary>
        /// <param name="mailname">用户名</param>
        /// <param name="parametername">权限名称</param>
        /// <param name="parametervalue">权限更改的值</param>
        /// <param name="skey"></param>
        /// <returns></returns>
        [HttpGet]
        public HttpResponseMessage SetMailbox(string mailname, string parametername, string parametervalue, string skey, string domain)
        {
            var message = string.Empty;
            var isSuccess = false;
            if (skey == admd5(domain))
            {
                var connInfo = mailexloginin(domain);
                var runspace = RunspaceFactory.CreateRunspace(connInfo);
                var command = new Command("set-mailbox");
                command.Parameters.Add("Identity", mailname);
                command.Parameters.Add(parametername, parametervalue);
                runspace.Open();
                var pipeline = runspace.CreatePipeline();
                pipeline.Commands.Add(command);
                var results = pipeline.Invoke();
                runspace.Dispose();
                isSuccess = true;
                message += "属性更新成功";
            }
            else
            {
                message = "API没经过授权无法调用!!!";
            }
            var result = new { isSuccess = isSuccess, message = message };
            HttpResponseMessage resultjson = toJson(result);
            return resultjson;
        }
        #endregion

        #region （41.1.2）Set-Mailbox
        /// <summary>
        /// 远程执行Set-Mailbox命令
        /// 修改用户邮箱容量数据库等信息
        /// </summary>
        /// <param name="mailname">用户名</param>
        /// <param name="parametername">权限名称</param>
        /// <param name="parametervalue">权限更改的值</param>
        /// <param name="skey"></param>
        /// <returns></returns>
        [HttpGet]
        public HttpResponseMessage SetMailboxback(string mailname, string parametername, string parametervalue, string skey, string domain)
        {
            var message = string.Empty;
            var isSuccess = false;
            if (skey == admd5(domain))
            {
                var connInfo = mailexloginin(domain);
                var runspace = RunspaceFactory.CreateRunspace(connInfo);
                var command = new Command("set-mailbox");
                command.Parameters.Add("Identity", mailname);
                command.Parameters.Add(parametername, parametervalue);
                runspace.Open();
                var pipeline = runspace.CreatePipeline();
                pipeline.Commands.Add(command);
                var results = pipeline.Invoke();
                runspace.Dispose();
                if (results.Count.ToString() != "1")
                {
                    message += "修改成功";
                }
                else
                {
                    isSuccess = true;
                    message = "修改失败";
                }
            }
            else
            {
                message = "API没经过授权无法调用!!!";
            }
            var result = new { isSuccess = isSuccess, message = message };
            HttpResponseMessage resultjson = toJson(result);
            return resultjson;
        }
        #endregion

        #region （60）CloseCASMailbox
        /// <summary>
        /// 远程执行Set-CASMailbox命令
        /// 修改用户移动设备
        /// </summary>
        /// <param name="mailname">用户名</param>
        /// <param name="skey"></param>
        /// <returns></returns>
        [HttpGet]
        public HttpResponseMessage CloseCASMailbox(string mailname, string skey, string domain)
        {
            var message = string.Empty;
            var isSuccess = false;
            if (skey == admd5(domain))
            {
                var connInfo = mailexloginin(domain);

                var runspace = RunspaceFactory.CreateRunspace(connInfo);
                //var command = new Command("Set-CASMailbox");
                //var command = new Command("Set-CASMailbox -Identity  ActiveSyncAllowedDeviceIDs  @{add='HVH6QOKJRD73N4QB2AMGKRH4T4'}");
                //command.Parameters.Add("Identity", mailname); 

                //command.Parameters.Add("ActiveSyncAllowedDeviceIDs",);
                //command.Parameters.Add("ActiveSyncAllowedDeviceIDs",new string[] { "HVH6QOKJRD73N4QB2AMGKRH4T4", "70PE47OGPD3PH40OPFEV6P99E0" });
                //command.Parameters.Add("ActiveSyncAllowedDeviceIDs", "@add=70PE47OGPD3PH40OPFEV6P99E0");
                runspace.Open();
                var pipeline = runspace.CreatePipeline();
                var parameters = "Set-CASMailbox -Identity " + mailname + " -ActiveSyncAllowedDeviceIDs 'id'";
                pipeline.Commands.AddScript(parameters);
                //pipeline.Commands.Add(command);
                var results = pipeline.Invoke();
                runspace.Dispose();
                isSuccess = true;
                message += "设备禁用成功";
            }
            else
            {
                message = "API没经过授权无法调用!!!";
            }
            var result = new { isSuccess = isSuccess, message = message };
            HttpResponseMessage resultjson = toJson(result);
            return resultjson;
        }
        #endregion
        #region (26)OU
        /// <summary>
        /// 点击前面加号加载数据
        /// </summary>
        /// <param name="path"></param>
        /// <param name="id"></param>
        /// <returns></returns>
        [HttpGet]
        public HttpResponseMessage GetobjectForOu(string path, string id, string domain)
        {
            try
            {
                DirectoryEntry de = GetDirectoryObjectforOU(path, domain);
                DirectorySearcher mySearcher = new DirectorySearcher(de);
                mySearcher.PageSize = 131512;//设置数量
                mySearcher.PropertiesToLoad.AddRange(new string[] { "name", "distinguishedName", "objectClass" });//这一句是指对范围内的属性进行加载，以提高效率。
                mySearcher.SearchScope = SearchScope.OneLevel;//设置搜索范围
                ArrayList mList = new ArrayList();
                int s = 1;
                mySearcher.Filter = ("(objectClass=organizationalUnit)"); //organizationalUnit          
                SearchResultCollection organizationalUnits = mySearcher.FindAll();
                foreach (System.DirectoryServices.SearchResult resEnt in organizationalUnits)
                {
                    var ids = id + s.ToString();
                    DirectoryEntry myDirectoryEntry = resEnt.GetDirectoryEntry();
                    var aduser =
                    new
                    {
                        id = Convert.ToInt32(ids),
                        pid = Convert.ToInt32(id),
                        name = myDirectoryEntry.Properties["name"].Value.ToString(),
                        path = myDirectoryEntry.Properties["distinguishedName"].Value.ToString(),
                        objectClass = "organizationalUnit",
                        isParent = true,
                    };
                    s++;
                    mList.Add(aduser);
                    myDirectoryEntry.Close();
                }
                mySearcher.Filter = ("(objectClass=group)"); //group          
                SearchResultCollection groups = mySearcher.FindAll();
                foreach (System.DirectoryServices.SearchResult resEnt in groups)
                {
                    var ids = id + s.ToString();
                    DirectoryEntry myDirectoryEntry = resEnt.GetDirectoryEntry();
                    var aduser =
                    new
                    {
                        id = Convert.ToInt32(ids),
                        pid = Convert.ToInt32(id),
                        name = myDirectoryEntry.Properties["name"].Value.ToString(),
                        path = myDirectoryEntry.Properties["distinguishedName"].Value.ToString(),
                        objectClass = "group",
                        isParent = false,
                    };
                    s++;
                    mList.Add(aduser);
                    myDirectoryEntry.Close();
                }
                mySearcher.Filter = ("(&(objectCategory=person)(objectClass=user))"); //user
                SearchResultCollection users = mySearcher.FindAll();
                foreach (System.DirectoryServices.SearchResult resEnt in users)
                {
                    var ids = id + s.ToString();
                    string icon = string.Empty;
                    DirectoryEntry myDirectoryEntry = resEnt.GetDirectoryEntry();
                    var intControl = Convert.ToInt32(myDirectoryEntry.Properties["userAccountControl"].Value.ToString());
                    //if (intControl == 512 || intControl == 544 || intControl == 4128 || intControl == 4096 || intControl == 69632 || intControl == 66048 || intControl == 66080 || intControl == 532480 || intControl == 2080)
                    //{
                    //    icon = "/static/zTreeStyle/img/user.png";
                    //}
                    //else
                    //{
                    //    icon = "/static/zTreeStyle/img/user2.png";
                    //}
                    //byte low = (byte)(intvalue & 0xFF);
                    var aduser =
                    new
                    {
                        id = Convert.ToInt32(ids),
                        pid = Convert.ToInt32(id),
                        name = myDirectoryEntry.Properties["name"].Value.ToString(),
                        path = myDirectoryEntry.Properties["distinguishedName"].Value.ToString(),
                        objectClass = "user",
                        icon = icon,
                        isParent = false,
                    };
                    s++;
                    mList.Add(aduser);
                    myDirectoryEntry.Close();

                }
                mySearcher.Filter = ("(objectClass=computer)"); //computer
                SearchResultCollection Computers = mySearcher.FindAll();
                foreach (System.DirectoryServices.SearchResult resEnt in Computers)
                {
                    var ids = id + s.ToString();
                    string icon = string.Empty;
                    DirectoryEntry myDirectoryEntry = resEnt.GetDirectoryEntry();
                    var intControl = Convert.ToInt32(myDirectoryEntry.Properties["userAccountControl"].Value.ToString());
                    //if (intControl == 512 || intControl == 544 || intControl == 4128 || intControl == 4096 || intControl == 69632 || intControl == 66048 || intControl == 66080 || intControl == 532480 || intControl == 2080)
                    //{
                    //    icon = "/static/zTreeStyle/img/Computer.png";
                    //}
                    //else
                    //{
                    //    icon = "/static/zTreeStyle/img/computer2.png";
                    //}
                    var aduser =
                    new
                    {
                        id = Convert.ToInt32(ids),
                        pid = Convert.ToInt32(id),
                        name = myDirectoryEntry.Properties["name"].Value.ToString(),
                        path = myDirectoryEntry.Properties["distinguishedName"].Value.ToString(),
                        objectClass = "computer",
                        icon = icon,
                        isParent = false,
                    };
                    s++;
                    mList.Add(aduser);
                    myDirectoryEntry.Close();

                }
                mySearcher.Filter = ("(objectClass=msExchDynamicDistributionList)"); //msExchDynamicDistributionList
                SearchResultCollection msExchstemMailboxs = mySearcher.FindAll();
                foreach (System.DirectoryServices.SearchResult resEnt in msExchstemMailboxs)
                {
                    var ids = id + s.ToString();
                    DirectoryEntry myDirectoryEntry = resEnt.GetDirectoryEntry();
                    var aduser =
                    new
                    {
                        id = Convert.ToInt32(ids),
                        pid = Convert.ToInt32(id),
                        name = myDirectoryEntry.Properties["name"].Value.ToString(),
                        path = myDirectoryEntry.Properties["distinguishedName"].Value.ToString(),
                        objectClass = "msExchDynamicDistributionList",
                        isParent = false,
                    };
                    s++;
                    mList.Add(aduser);
                    myDirectoryEntry.Close();

                }
                de.Close();
                var isSuccess = true;
                var result = new { isSuccess = isSuccess, message = mList };
                HttpResponseMessage resultjson = toJson(result);
                return resultjson;
            }
            catch (Exception ex)
            {
                var result = new { isSuccess = false, message = ex.Message };
                HttpResponseMessage resultjson = toJson(result);
                return resultjson;
            }
        }
        #endregion

        #region (27)接口存活测试
        /// <summary>
        /// 接口存活测试
        /// 并修改web.config
        /// </summary>
        /// 
        public bool set_config(string server, string Database, string PORT, string Uid, string password)
        {
            var result = false;
            try
            {
                Configuration config = WebConfigurationManager.OpenWebConfiguration("~");
                AppSettingsSection app = config.AppSettings;
                app.Settings["server"].Value = server;
                app.Settings["Database"].Value = Database;
                app.Settings["PORT"].Value = PORT;
                app.Settings["Uid"].Value = Uid;
                app.Settings["password"].Value = password;
                config.Save(ConfigurationSaveMode.Modified);
                Mysqldbinfo dbinfo = new Mysqldbinfo();
                var mysql_globals = dbinfo.Selglobals();
                if (mysql_globals["isSuccess"] == "True") {
                    result = true;
                }
            }
            catch (Exception)
            {
                result = false;
            }
            return result;
        }

        [HttpGet]
        public HttpResponseMessage OnLineTest(string server, string Database, string PORT, string Uid, string password, string skey)
        {
            var result = false;
            try
            {
                
                Mysqldbinfo dbinfo = new Mysqldbinfo();
                var mysql_globals = dbinfo.Selglobals();

                if (mysql_globals["isSuccess"] == "True")
                {
                    if (mysql_globals["skey"] == skey)
                    {
                        result = set_config(server, Database, PORT,  Uid,  password);
                    }
                    
                }
                else
                {
                    result = set_config(server, Database, PORT, Uid, password);
                }
            }
            catch (Exception )
            {
                result = false;
            }
            HttpResponseMessage resultjson = toJson(result);
            return resultjson;
        }

        #endregion

        #region (27.1)iis测试
        /// <summary>
        /// 接口存活测试
        /// 并修改web.config
        /// </summary>
        /// 
        [HttpGet]
        public HttpResponseMessage iisonlinetest()
        {
            bool result = true;
            HttpResponseMessage resultjson = toJson(result);
            return resultjson;
        }

        #endregion

        #region （56）Get-ActiveSync
        /// <summary>
        /// 远程执行Get-ActiveSync
        /// 获取用户手机id
        /// </summary>
        /// <param name="mailname">用户名</param>
        /// <param name="parametername">权限名称</param>
        /// <param name="skey"></param>
        /// <returns></returns>
        [HttpGet]
        public HttpResponseMessage GetActiveSyncDevice(string mailname, string parametername, string skey, string domain)
        {
            List<object> message = new List<object>();
            var isSuccess = false;
            if (skey == admd5(domain))
            {

                var connInfo = mailexloginin(domain);
                var runspace = RunspaceFactory.CreateRunspace(connInfo);
                var command = new Command("Get-ActiveSyncDevice");
                command.Parameters.Add("Mailbox", mailname);
                //command.Parameters.Add("Alias", sGroup);
                runspace.Open();
                var pipeline = runspace.CreatePipeline();
                pipeline.Commands.Add(command);
                var results = pipeline.Invoke();
                runspace.Dispose();
                if (results.Count.ToString() == "0")
                {
                    message.Add("无移动设备信息");
                }
                else
                {
                    for (int i = 0; i < int.Parse(results.Count.ToString()); i++)
                        try
                        {
                            var aaa = new { DeviceId = results[i].Members[parametername].Value, Creatime = DateTime.Parse(results[i].Members["FirstSyncTime"].Value.ToString()).AddHours(8).ToString(), state = results[i].Members["DeviceAccessState"].Value, DeviceModel = results[i].Members["DeviceModel"].Value };
                            message.Add(aaa);
                            //message.Add("{'DeviceId':'" + results[i].Members[parametername].Value + "','Creatime':'" + results[i].Members["FirstSyncTime"].Value + "','state':'" + results[i].Members["DeviceAccessState"].Value + "','DeviceModel':'" + results[i].Members["DeviceModel"].Value + "'}");
                            //message += results[0].Members[parametername].Value;
                            isSuccess = true;
                        }
                        catch (Exception)
                        {
                            message.Add("权限不存在");
                            var result1 = new { isSuccess = isSuccess, message = message };
                            HttpResponseMessage resultjson1 = toJson(result1);
                            return resultjson1;
                        }

                }
            }
            else
            {
                message.Add("API没经过授权无法调用!!!");
            }
            var result = new { isSuccess = isSuccess, message = message };
            HttpResponseMessage resultjson = toJson(result);
            return resultjson;
        }
        #endregion


        #region （56.5）Get-MailBox
        /// <summary>
        /// 远程执行GetMailBox
        /// </summary>
        /// <param name="mailname">用户名</param>
        /// <param name="parametername">权限名称</param>
        /// <param name="skey"></param>
        /// <returns></returns>
        [HttpGet]
        public HttpResponseMessage GetMailBox(string mailname,  string skey, string domain)
        {
            List<object> message = new List<object>();
            var isSuccess = false;
            if (skey == admd5(domain))
            {

                var connInfo = mailexloginin(domain);
                var runspace = RunspaceFactory.CreateRunspace(connInfo);
                var command = new Command("Get-MailBox");
                command.Parameters.Add("Identity", mailname);
                //command.Parameters.Add("Alias", sGroup);
                runspace.Open();
                var pipeline = runspace.CreatePipeline();
                pipeline.Commands.Add(command);
                var results = pipeline.Invoke();
                runspace.Dispose();
                if (results.Count.ToString() == "0")
                {
                    message.Add("无权限信息");
                }
                else
                {
                    for (int i = 0; i < int.Parse(results.Count.ToString()); i++)
                        try
                        {
                            var aaa = new { DisplayName = results[i].Members["DisplayName"].Value, SamAccountName = results[i].Members["SamAccountName"].Value, PrimarySmtpAddress = results[i].Members["PrimarySmtpAddress"].Value, };
                            message.Add(aaa);
                            //message.Add("{'DeviceId':'" + results[i].Members[parametername].Value + "','Creatime':'" + results[i].Members["FirstSyncTime"].Value + "','state':'" + results[i].Members["DeviceAccessState"].Value + "','DeviceModel':'" + results[i].Members["DeviceModel"].Value + "'}");
                            //message += results[0].Members[parametername].Value;
                            isSuccess = true;
                        }
                        catch (Exception)
                        {
                            message.Add("权限不存在");
                            var result1 = new { isSuccess = isSuccess, message = message };
                            HttpResponseMessage resultjson1 = toJson(result1);
                            return resultjson1;
                        }

                }
            }
            else
            {
                message.Add("API没经过授权无法调用!!!");
            }
            var result = new { isSuccess = isSuccess, message = message };
            HttpResponseMessage resultjson = toJson(result);
            return resultjson;
        }
        #endregion



        #region （61）Set-CASMailbox
        /// <summary>
        /// 远程执行Set-CASMailbox命令
        /// 修改用户移动设备
        /// </summary>
        /// <param name="mailname">用户名</param>
        /// <param name="skey"></param>
        /// <returns></returns>
        [HttpGet]
        public HttpResponseMessage SetCASMailbox(string mailname, string id, string skey, string domain)
        {
            var message = string.Empty;
            var isSuccess = false;
            if (skey == admd5(domain))
            {
                var connInfo = mailexloginin(domain);

                var runspace = RunspaceFactory.CreateRunspace(connInfo);
                //var command = new Command("Set-CASMailbox");
                //var command = new Command("Set-CASMailbox -Identity  ActiveSyncAllowedDeviceIDs  @{add='HVH6QOKJRD73N4QB2AMGKRH4T4'}");
                //command.Parameters.Add("Identity", mailname); 

                //command.Parameters.Add("ActiveSyncAllowedDeviceIDs",);
                //command.Parameters.Add("ActiveSyncAllowedDeviceIDs",new string[] { "HVH6QOKJRD73N4QB2AMGKRH4T4", "70PE47OGPD3PH40OPFEV6P99E0" });
                //command.Parameters.Add("ActiveSyncAllowedDeviceIDs", "@add=70PE47OGPD3PH40OPFEV6P99E0");
                runspace.Open();
                var pipeline = runspace.CreatePipeline();
                var parameters = "Set-CASMailbox -Identity " + mailname + " -ActiveSyncAllowedDeviceIDs  @{add='" + id + "'}";
                pipeline.Commands.AddScript(parameters);
                //pipeline.Commands.Add(command);
                var results = pipeline.Invoke();
                runspace.Dispose();
                isSuccess = true;
                message += "设备解锁成功";
            }
            else
            {
                message = "API没经过授权无法调用!!!";
            }
            var result = new { isSuccess = isSuccess, message = message };
            HttpResponseMessage resultjson = toJson(result);
            return resultjson;
        }
        #endregion

        #region （61.1）Set-DistributionGroup
        /// <summary>
        /// 远程执行Set-DistributionGroup命令
        /// </summary>
        /// <param name="mailname">用户名</param>
        /// <param name="skey"></param>
        /// <returns></returns>
        [HttpGet]
        public HttpResponseMessage SetDistributionGroupaddremove(string mailname, string id,string projectname1,string todo, string skey, string domain)
        {
            try
            {
                var message = string.Empty;
                var isSuccess = false;
                if (skey == admd5(domain))
                {
                    var connInfo = mailexloginin(domain);

                    var runspace = RunspaceFactory.CreateRunspace(connInfo);
                    runspace.Open();
                    var pipeline = runspace.CreatePipeline();
                    var parameters = "Set-DistributionGroup -Identity " + mailname + " -" + projectname1 + "  @{"+ todo + "='" + id + "'}";
                    pipeline.Commands.AddScript(parameters);
                    //pipeline.Commands.Add(command);
                    var results = pipeline.Invoke();
                    runspace.Dispose();
                    if (results.Count.ToString() == "0")
                    {
                        isSuccess = true;
                    }
                    else
                    {
                        isSuccess = false;
                    }
                }
                else
                {
                    isSuccess = false;
                    message = "API没经过授权无法调用!!!";
                }
                var result = new { isSuccess = isSuccess };
                HttpResponseMessage resultjson = toJson(result);
                return resultjson;
            }
            catch (Exception)
            {
                bool isSuccess = false;
                var result = new { isSuccess = isSuccess };
                HttpResponseMessage resultjson = toJson(result);
                return resultjson;
            }
        }
        #endregion


        #region (62) 测试ad链接
        [HttpGet]
        public HttpResponseMessage adlinktest(string adip, string account, string password, string domain, string adpath, string skey)
        {
            try
            {
                bool isSuccess = true;

                if (skey == admd5_nodomain())
                {
                    DirectoryEntry entry = new DirectoryEntry("LDAP://" + adip + "/" + adpath, domain + "\\" + account, password, AuthenticationTypes.Secure);


                    DirectorySearcher deSearch = new DirectorySearcher();
                    deSearch.SearchRoot = entry;
                    deSearch.Filter = "(|(&(objectClass=user)(objectCategory=person) (|(sAMAccountName=" + account + ")(cn=" + account + "))))";
                    SearchResultCollection results = deSearch.FindAll();
                    entry.Close();
                    if (results.Count == 0)
                    {
                        isSuccess = false;
                    }
                }
                else
                {
                    isSuccess = false;
                }

                var result = new { isSuccess = isSuccess };
                HttpResponseMessage resultjson = toJson(result);
                return resultjson;
            }

            catch (Exception)
            {
                bool isSuccess = false;
                var result = new { isSuccess = isSuccess };
                HttpResponseMessage resultjson = toJson(result);
                return resultjson;
            }
        }
        #endregion


        #region （63）Get-mailbox测试
        /// <summary>
        /// Get-mailbox测试
        /// </summary>
        /// <param name="mailname">用户名</param>
        /// <param name="parametername">权限名称</param>
        /// <param name="skey"></param>
        /// <returns></returns>
        [HttpGet]
        public HttpResponseMessage testexlink(string exip, string exaccount, string expassword, string skey, string domain)
        {
            try
            {
                var isSuccess = true;
                if (skey == admd5(domain))
                {

                    SecureString ssRunasPassword = new SecureString();
                    foreach (char x in expassword)
                    {
                        ssRunasPassword.AppendChar(x);
                    }
                    PSCredential credentials = new PSCredential(domain + "\\" + exaccount, ssRunasPassword);
                    //var connInfo = new WSManConnectionInfo(new Uri("http://0.0.0.0/PowerShell"), "http://schemas.microsoft.com/powershell/Microsoft.Exchange", credentials);
                    var connInfo = new WSManConnectionInfo(new Uri("http://" + exip + "/PowerShell"), "http://schemas.microsoft.com/powershell/Microsoft.Exchange", credentials);
                    connInfo.AuthenticationMechanism = AuthenticationMechanism.Basic;
                    var runspace = RunspaceFactory.CreateRunspace(connInfo);
                    var command = new Command("Get-Mailbox");
                    command.Parameters.Add("Identity", exaccount);
                    //command.Parameters.Add("Alias", sGroup);
                    runspace.Open();
                    var pipeline = runspace.CreatePipeline();
                    pipeline.Commands.Add(command);
                    var results = pipeline.Invoke();
                    runspace.Dispose();
                    if (results.Count.ToString() == "0")
                    {
                        isSuccess = false;
                    }
                }
                else
                {
                    isSuccess = false;
                }
                var result = new { isSuccess = isSuccess };
                HttpResponseMessage resultjson = toJson(result);
                return resultjson;
            }
            catch (Exception)
            {
                bool isSuccess = false;
                var result = new { isSuccess = isSuccess };
                HttpResponseMessage resultjson = toJson(result);
                return resultjson;
            }
        }
        #endregion

        #region (65)根据传入的ladp 来查找属性
        //根据传入的ladp 来查找属性 实体
        public class LdapsObject
        {
            public string ldaps { get; set; }
            public string skey { get; set; }
            public string domain { get; set; }
            public string path { get; set; }
            public int limit { get; set; }
            public String[] Properties { get; set; }
        }

        [HttpPost]
        public HttpResponseMessage GetUserFromLdap(LdapsObject LdapsObjects)
        {
            var isSuccess = false;
            if (LdapsObjects.skey == admd5(LdapsObjects.domain))
            {
                try
                {
                    DirectoryEntry de = GetDirectoryObjectforOU(LdapsObjects.path, LdapsObjects.domain);//获取AD传入路径的实体
                    DirectorySearcher deSearch = new DirectorySearcher(de); //搜索
                    deSearch.PageSize = 1315120;//设置单页访问数量
                    deSearch.SizeLimit = LdapsObjects.limit;//设置数量
                    deSearch.SearchScope = SearchScope.Subtree;//设置搜索范围 OneLevel 本层  Subtree 树状
                    deSearch.Filter = LdapsObjects.ldaps; //ldaps 语句 例：(&(objectCategory=person)(objectClass=user) (sAMAccountName=""))
                    deSearch.PropertiesToLoad.AddRange(new string[] { "sAMAccountName", "distinguishedName", "objectClass", "cn", "description", "mail", "sn", "givenName", "userPrincipalName", "displayName", "wWWHomePage", "physicalDeliveryOfficeName", "memberof", "userAccountControl", "member" });//这一句是指对范围内的属性进行加载，以提高效率。
                    //deSearch.PropertiesToLoad.Clear();
                    SearchResultCollection deSearchs = deSearch.FindAll();//ldaps 查询到所有的
                    ArrayList mList = new ArrayList();

                    var AdCount = deSearchs.Count;

                    foreach (System.DirectoryServices.SearchResult resEnt in deSearchs)
                    {
                        ResultPropertyCollection ResultPropColl = resEnt.Properties;
                        Dictionary<string, object> AdPropertieDictionary = new Dictionary<string, object>();
                        foreach (string myKey in ResultPropColl.PropertyNames)
                        {
                            //if (myKey== "whencreated"|| myKey == "whenchanged")
                            //{
                            //    System.DateTime AdPropertiejDateTimes = ((DateTime)ResultPropColl[myKey][0]).AddHours(+8);
                            //    AdPropertieDictionary.Add(myKey, AdPropertiejDateTimes.ToString());
                            //}
                            //else
                            //{
                            AdPropertieDictionary.Add(myKey, ResultPropColl[myKey]);
                            //}
                        }
                        mList.Add(AdPropertieDictionary);
                    }
                    deSearch.Dispose();
                    de.Dispose();
                    de.Close();
                    var result = new { isSuccess = true, message = mList, Count = AdCount };
                    HttpResponseMessage resultjson = toJson(result);
                    return resultjson;
                }
                catch (Exception ex)
                {
                    var message = new { message = ex.Message };
                    var result = new { isSuccess = isSuccess, message = message };
                    HttpResponseMessage resultjson = toJson(result);
                    return resultjson;
                }
            }
            else
            {
                var message = new { message = "API没经过授权无法调用!!!" };
                var result = new { isSuccess = isSuccess, message = message };
                HttpResponseMessage resultjson = toJson(result);
                return resultjson;
            }
        }
        [HttpPost]
        public HttpResponseMessage GetUserFromLdapToLoad(LdapsObject LdapsObjects)
        {
            var isSuccess = false;
            if (LdapsObjects.skey == admd5(LdapsObjects.domain))
            {
                try
                {
                    DirectoryEntry de = GetDirectoryObjectforOU(LdapsObjects.path, LdapsObjects.domain);//获取AD传入路径的实体
                    DirectorySearcher deSearch = new DirectorySearcher(de); //搜索
                    deSearch.PageSize = 1315120;//设置单页访问数量
                    deSearch.SizeLimit = LdapsObjects.limit;//设置数量
                    deSearch.SearchScope = SearchScope.Subtree;//设置搜索范围 OneLevel 本层  Subtree 树状
                    deSearch.Filter = LdapsObjects.ldaps; //ldaps 语句 例：(&(objectCategory=person)(objectClass=user) (sAMAccountName=""))
                    //deSearch.PropertiesToLoad.Add("sAMAccountName");
                    try
                    {
                        if (LdapsObjects.Properties[0] != "" && LdapsObjects.Properties[0] != null && LdapsObjects.Properties[0] != "None")
                        {
                            deSearch.PropertiesToLoad.AddRange(LdapsObjects.Properties);
                            deSearch.PropertiesToLoad.Remove("ADsPath");//这一句是指对范围内的属性进行加载，以提高效率。
                        }
                    }
                    catch (Exception)
                    {

                    }
                    //deSearch.PropertiesToLoad.Clear();
                    SearchResultCollection deSearchs = deSearch.FindAll();//ldaps 查询到所有的
                    ArrayList mList = new ArrayList();
                    var AdCount = deSearchs.Count;
                    foreach (System.DirectoryServices.SearchResult resEnt in deSearchs)
                    {
                        ResultPropertyCollection ResultPropColl = resEnt.Properties;
                        Dictionary<string, object> AdPropertieDictionary = new Dictionary<string, object>();
                        foreach (string myKey in ResultPropColl.PropertyNames)
                        {
                            //if (myKey== "whencreated"|| myKey == "whenchanged")
                            //{
                            //    System.DateTime AdPropertiejDateTimes = ((DateTime)ResultPropColl[myKey][0]).AddHours(+8);
                            //    AdPropertieDictionary.Add(myKey, AdPropertiejDateTimes.ToString());
                            //}
                            //else
                            //{
                            AdPropertieDictionary.Add(myKey, ResultPropColl[myKey]);
                            //}
                        }
                        mList.Add(AdPropertieDictionary);
                    }
                    deSearch.Dispose();
                    de.Dispose();
                    de.Close();
                    var result = new { isSuccess = true, message = mList, Count = AdCount };
                    HttpResponseMessage resultjson = toJson(result);
                    return resultjson;
                }
                catch (Exception ex)
                {
                    var message = new { message = ex.Message };
                    var result = new { isSuccess = isSuccess, message = message };
                    HttpResponseMessage resultjson = toJson(result);
                    return resultjson;
                }
            }
            else
            {
                var message = new { message = "API没经过授权无法调用!!!" };
                var result = new { isSuccess = isSuccess, message = message };
                HttpResponseMessage resultjson = toJson(result);
                return resultjson;
            }
        }

        [HttpPost]
        public HttpResponseMessage GetUserpasswordexpirationdate(LdapsObject LdapsObjects)
        {
            var isSuccess = false;
            if (LdapsObjects.skey == admd5(LdapsObjects.domain))
            {
                try
                {
                    DirectoryEntry de = GetDirectoryObjectforOU(LdapsObjects.path, LdapsObjects.domain);//获取AD传入路径的实体
                    DirectorySearcher deSearch = new DirectorySearcher(de); //搜索
                    deSearch.PageSize = 1315120;//设置单页访问数量
                    deSearch.SizeLimit = LdapsObjects.limit;//设置数量
                    deSearch.SearchScope = SearchScope.Subtree;//设置搜索范围 OneLevel 本层  Subtree 树状
                    deSearch.Filter = LdapsObjects.ldaps; //ldaps 语句 例：(&(objectCategory=person)(objectClass=user) (sAMAccountName=""))
                    //deSearch.PropertiesToLoad.Add("sAMAccountName");
                    try
                    {
                        if (LdapsObjects.Properties[0] != "" && LdapsObjects.Properties[0] != null && LdapsObjects.Properties[0] != "None")
                        {
                            deSearch.PropertiesToLoad.AddRange(LdapsObjects.Properties);//这一句是指对范围内的属性进行加载，以提高效率。
                        }
                    }
                    catch (Exception)
                    {

                    }
                    //deSearch.PropertiesToLoad.Clear();
                    SearchResultCollection deSearchs = deSearch.FindAll();//ldaps 查询到所有的
                    ArrayList mList = new ArrayList();

                    var AdCount = deSearchs.Count;

                    foreach (System.DirectoryServices.SearchResult resEnt in deSearchs)
                    {
                        ResultPropertyCollection ResultPropColl = resEnt.Properties;
                        Dictionary<string, object> AdPropertieDictionary = new Dictionary<string, object>();
                        if (LdapsObjects.Properties.Contains("passwordexpirationdate"))
                        {
                            DirectoryEntry deresEnt = resEnt.GetDirectoryEntry();
                            string passwordexpirationdate = deresEnt.InvokeGet("passwordexpirationdate").ToString(); //获取密码到期时间
                            AdPropertieDictionary.Add("passwordexpirationdate", new string[] { passwordexpirationdate });
                            deresEnt.Dispose();
                            deresEnt.Close();
                        }
                        foreach (string myKey in ResultPropColl.PropertyNames)
                        {
                            //if (myKey== "whencreated"|| myKey == "whenchanged")
                            //{
                            //    System.DateTime AdPropertiejDateTimes = ((DateTime)ResultPropColl[myKey][0]).AddHours(+8);
                            //    AdPropertieDictionary.Add(myKey, AdPropertiejDateTimes.ToString());
                            //}
                            //else
                            //{
                            AdPropertieDictionary.Add(myKey, ResultPropColl[myKey]);
                            //}
                        }
                        mList.Add(AdPropertieDictionary);
                    }
                    deSearch.Dispose();
                    de.Dispose();
                    de.Close();
                    var result = new { isSuccess = true, message = mList, Count = AdCount };
                    HttpResponseMessage resultjson = toJson(result);
                    return resultjson;
                }
                catch (Exception ex)
                {
                    var message = new { message = ex.Message };
                    var result = new { isSuccess = isSuccess, message = message };
                    HttpResponseMessage resultjson = toJson(result);
                    return resultjson;
                }
            }
            else
            {
                var message = new { message = "API没经过授权无法调用!!!" };
                var result = new { isSuccess = isSuccess, message = message };
                HttpResponseMessage resultjson = toJson(result);
                return resultjson;
            }
        }

        #endregion


        #region (66)new-DistributionGroup 新建群组
        /// <summary>
        /// Set-Mailbox
        ///  这个账号是否显示在Exchange通讯簿上
        /// </summary>
        /// <param name="Identity">用户名</param>

        [HttpGet]
        public HttpResponseMessage newDistributionGroup(string Alias, string DisplayName,string ManagedBy,string OrganizationalUnit,  string skey, string domain)
        {
            var message = string.Empty;
            var isSuccess = false;
            if (skey == admd5(domain))
            {

                var connInfo = mailexloginin(domain);
                var runspace = RunspaceFactory.CreateRunspace(connInfo);
                var command = new Command("new-DistributionGroup");
                command.Parameters.Add("Name", Alias);
                command.Parameters.Add("SamAccountName", Alias);
                command.Parameters.Add("Alias", Alias);
                command.Parameters.Add("DisplayName", DisplayName);
                command.Parameters.Add("ManagedBy", ManagedBy);
                if (OrganizationalUnit != "None")
                {
                    command.Parameters.Add("OrganizationalUnit", OrganizationalUnit);
                }
                runspace.Open();
                var pipeline = runspace.CreatePipeline();
                pipeline.Commands.Add(command);
                var results = pipeline.Invoke();
                runspace.Dispose();
                if (results.Count.ToString() != "0")
                {
                    isSuccess = true;
                    message = "创建成功";
                }
                else
                {
                    message += "创建错误";
                }
            }
            else
            {
                message = "API没经过授权无法调用!!!";
            }
            var result = new { isSuccess = isSuccess, message = message };
            HttpResponseMessage resultjson = toJson(result);
            return resultjson;
        }

        #endregion

        #region (67)根据对象类别查找accountExpires属性
        [HttpGet]
        public HttpResponseMessage GetuseraccountExpires(string objects,string skey, string domain)
        {
            var isSuccess = false;
            if (skey == admd5(domain))
            {
               
                try
                {
                    
                    DirectoryEntry oUser = GetDirectoryEntryOfUser(objects, domain).GetDirectoryEntry();
                    var accountExpires = (GetDateTimeFromLargeInteger((IADsLargeInteger)oUser.Properties["accountExpires"].Value).AddHours(+8)).ToString();
                    oUser.CommitChanges();
                    oUser.Close();
                    var result = new { isSuccess = true, message = accountExpires };
                    HttpResponseMessage resultjson = toJson(result);
                    return resultjson;
                }
                catch (Exception ex)
                {
                    var message = new { message = ex.Message };
                    var result = new { isSuccess = isSuccess, message = message };
                    HttpResponseMessage resultjson = toJson(result);
                    return resultjson;
                }
            }
            else
            {
                var message = new { message = "API没经过授权无法调用!!!" };
                var result = new { isSuccess = isSuccess, message = message };
                HttpResponseMessage resultjson = toJson(result);
                return resultjson;
            }
        }
        #endregion

        #region (68)根据对象类别查找属性
        [HttpGet]
        public HttpResponseMessage Getuseraccountfornovalue(string objects, string returnvalue, string skey, string domain)
        {
            var isSuccess = false;
            if (skey == admd5(domain))
            {

                try
                {
                    DirectoryEntry oUser = GetDirectoryEntryOfUser(objects, domain).GetDirectoryEntry();
                    oUser.CommitChanges();
                    var returnvaluelast = oUser.Properties["physicalDeliveryOfficeName"].Value;                        
                    oUser.Close();
                    isSuccess = true;
                
                var result = new { isSuccess = true, message = returnvaluelast };
                    HttpResponseMessage resultjson = toJson(result);
                    return resultjson;
                }
                catch (Exception ex)
                {
                    var message = new { message = ex.Message };
                    var result = new { isSuccess = isSuccess, message = message };
                    HttpResponseMessage resultjson = toJson(result);
                    return resultjson;
                }
            }
            else
            {
                var message = new { message = "API没经过授权无法调用!!!" };
                var result = new { isSuccess = isSuccess, message = message };
                HttpResponseMessage resultjson = toJson(result);
                return resultjson;
            }
        }
        #endregion

    }
} 