using System;
using System.Configuration;
using System.Web.Configuration;
using System.Collections.Generic;
using MySql.Data.MySqlClient;
using System.Data;
using System.Security.Cryptography;
using System.Text;
using open_itapi.Controllers;

namespace Mysqlapi.Controllers
{

    public class Mysqldbinfo
    {
        #region (61)web.config 配置
        public Dictionary<string, string> get_globals()
        {
            try
            {
                Dictionary<string, string> mysql_globals = new Dictionary<string, string>();
                mysql_globals.Add("server", ConfigurationManager.AppSettings["server"]);
                mysql_globals.Add("Database", ConfigurationManager.AppSettings["Database"]);
                mysql_globals.Add("PORT", ConfigurationManager.AppSettings["PORT"]);
                mysql_globals.Add("Uid", ConfigurationManager.AppSettings["Uid"]);
                AdapiController ADapi = new AdapiController();
                string password = ADapi.Decrypction(ConfigurationManager.AppSettings["password"]);
                mysql_globals.Add("password", password);
                return mysql_globals;
            }
            catch (Exception)
            {
                Dictionary<string, string> mysql_globals = new Dictionary<string, string>();
                return mysql_globals;
            }
        }

        #endregion

        #region mysql数据库操作
        /// <summary>
        /// 链接数据库
        /// </summary>
        /// <returns></returns>
        public MySqlConnection mysqlcon()
        {
            Dictionary<string, string> mysql_globals =  get_globals();
            string constr = "server="+ mysql_globals["server"] + ";Database=" + mysql_globals["Database"] + ";PORT=" + mysql_globals["PORT"] + ";Uid=" + mysql_globals["Uid"] + ";password=" + mysql_globals["password"] + ";charset=utf8";
            MySqlConnection mycon = new MySqlConnection(constr);
            return mycon;
        }
        /// <summary>
        /// 获取AD参数
        /// </summary>
        /// <param name="domain"></param>
        /// <returns></returns>
        public Dictionary<string, string> Selglobals()
        {
            try
            {
                MySqlConnection mycon = mysqlcon();
                mycon.Open();
                string sql1 = string.Format(@"SELECT * FROM global_configuration LIMIT 1");
                MySqlCommand mycmd = new MySqlCommand(sql1, mycon);
                MySqlDataAdapter ada = new MySqlDataAdapter(mycmd);
                DataSet ds = new DataSet();
                ada.Fill(ds, "table");
                Dictionary<string, string> tabledict = new Dictionary<string, string>();
                foreach (DataTable table in ds.Tables)
                {
                    foreach (DataRow row in table.Rows)
                    {
                        foreach (DataColumn column in table.Columns)

                        {
                            if (column.ToString() == "ad_password" || column.ToString() == "ex_password") {
                                AdapiController ADapi = new AdapiController();
                                string password = ADapi.Decrypction(row[column].ToString());
                                tabledict.Add(column.ToString(), password);
                            }
                            else
                            {
                                tabledict.Add(column.ToString(), row[column].ToString());
                            }
                            
                        }
                    }
                }
                mycon.Close();
                var fulldomain = "@"+tabledict["ad_path"].Replace("DC=","").Replace(",",".");
                tabledict.Add("fulldomain", fulldomain);
                string _ldapIdentity = @"LDAP://"+tabledict["ad_ip"]+"/";
                tabledict.Add("_ldapIdentity", _ldapIdentity);
                tabledict.Add("isSuccess", "True");
                return tabledict;
            }
            catch (Exception ex)
            {
                var message = ex.Message;
                Dictionary<string, string> tabledict = new Dictionary<string, string>();
                tabledict.Add("isSuccess", "False");
                tabledict.Add("message", message);
                return tabledict;
            }
        }

        public Dictionary<string, string> Selglobals_noDecrypction()
        {
            try
            {
                MySqlConnection mycon = mysqlcon();
                mycon.Open();
                string sql1 = string.Format(@"SELECT * FROM global_configuration LIMIT 1");
                MySqlCommand mycmd = new MySqlCommand(sql1, mycon);
                MySqlDataAdapter ada = new MySqlDataAdapter(mycmd);
                DataSet ds = new DataSet();
                ada.Fill(ds, "table");
                Dictionary<string, string> tabledict = new Dictionary<string, string>();
                foreach (DataTable table in ds.Tables)
                {
                    foreach (DataRow row in table.Rows)
                    {
                        foreach (DataColumn column in table.Columns)

                        {
                                tabledict.Add(column.ToString(), row[column].ToString());                            

                        }
                    }
                }
                mycon.Close();
                var fulldomain = "@" + tabledict["ad_path"].Replace("DC=", "").Replace(",", ".");
                tabledict.Add("fulldomain", fulldomain);
                string _ldapIdentity = @"LDAP://" + tabledict["ad_ip"] + "/";
                tabledict.Add("_ldapIdentity", _ldapIdentity);
                tabledict.Add("isSuccess", "True");
                return tabledict;
            }
            catch (Exception ex)
            {
                var message = ex.Message;
                Dictionary<string, string> tabledict = new Dictionary<string, string>();
                tabledict.Add("isSuccess", "False");
                tabledict.Add("message", message);
                return tabledict;
            }
        }
        public Dictionary<string, string> Selglobals(string domain)
        {
            try
            {
                MySqlConnection mycon = mysqlcon();
                mycon.Open();
                string sql1 = string.Format(@"SELECT * FROM global_configuration where ad_domain='{0}' LIMIT 1", domain);
                MySqlCommand mycmd = new MySqlCommand(sql1, mycon);
                MySqlDataAdapter ada = new MySqlDataAdapter(mycmd);
                DataSet ds = new DataSet();
                ada.Fill(ds, "table");
                Dictionary<string, string> tabledict = new Dictionary<string, string>();
                foreach (DataTable table in ds.Tables)
                {
                    foreach (DataRow row in table.Rows)
                    {
                        foreach (DataColumn column in table.Columns)

                        {
                            if (column.ToString() == "ad_password" || column.ToString() == "ex_password")
                            {
                                AdapiController ADapi = new AdapiController();
                                string password = ADapi.Decrypction(row[column].ToString());
                                tabledict.Add(column.ToString(), password);
                            }
                            else
                            {
                                tabledict.Add(column.ToString(), row[column].ToString());
                            }

                        }
                    }
                }
                mycon.Close();
                var fulldomain = "@" + tabledict["ad_path"].Replace("DC=", "").Replace(",", ".");
                tabledict.Add("fulldomain", fulldomain);
                string _ldapIdentity = @"LDAP://" + tabledict["ad_ip"] + "/";
                tabledict.Add("_ldapIdentity", _ldapIdentity);
                tabledict.Add("isSuccess", "True");
                return tabledict;
            }
            catch (Exception ex)
            {
                var message = ex.Message;
                Dictionary<string, string> tabledict = new Dictionary<string, string>();
                tabledict.Add("isSuccess", "False");
                tabledict.Add("message", message);
                return tabledict;
            }
        }

        public Dictionary<string, string> Selglobalsnocolumn(string domain)
        {
            try
            {
                MySqlConnection mycon = mysqlcon();
                mycon.Open();
                string sql1 = string.Format(@"SELECT * FROM global_configuration where ad_domain='{0}' LIMIT 1", domain);
                MySqlCommand mycmd = new MySqlCommand(sql1, mycon);
                MySqlDataAdapter ada = new MySqlDataAdapter(mycmd);
                DataSet ds = new DataSet();
                ada.Fill(ds, "table");
                Dictionary<string, string> tabledict = new Dictionary<string, string>();
                foreach (DataTable table in ds.Tables)
                {
                    foreach (DataRow row in table.Rows)
                    {
                        foreach (DataColumn column in table.Columns)

                        {
                                tabledict.Add(column.ToString(), row[column].ToString());
                            

                        }
                    }
                }
                mycon.Close();
                var fulldomain = "@" + tabledict["ad_path"].Replace("DC=", "").Replace(",", ".");
                tabledict.Add("fulldomain", fulldomain);
                string _ldapIdentity = @"LDAP://" + tabledict["ad_ip"] + "/";
                tabledict.Add("_ldapIdentity", _ldapIdentity);
                tabledict.Add("isSuccess", "True");
                return tabledict;
            }
            catch (Exception ex)
            {
                var message = ex.Message;
                Dictionary<string, string> tabledict = new Dictionary<string, string>();
                tabledict.Add("isSuccess", "False");
                tabledict.Add("message", message);
                return tabledict;
            }
        }
        /// <summary>
        /// 获取AD参数
        /// </summary>
        /// <param name="domain"></param>
        /// <returns></returns>
        public Dictionary<string, string> SelServerConfig(string domain)
        {
            try
            {
                MySqlConnection mycon = mysqlcon();
                mycon.Open();
                string sql1 = string.Format(@"SELECT * FROM ad_configuration where domain='{0}'", domain);
                MySqlCommand mycmd = new MySqlCommand(sql1, mycon);
                MySqlDataAdapter ada = new MySqlDataAdapter(mycmd);
                DataSet ds = new DataSet();
                ada.Fill(ds, "table");
                Dictionary<string, string> tabledict = new Dictionary<string, string>();
                foreach (DataTable table in ds.Tables)
                {
                    foreach (DataRow row in table.Rows)
                    {
                        foreach (DataColumn column in table.Columns)

                        {
                            tabledict.Add(column.ToString(), row[column].ToString());
                        }
                    }
                }
                mycon.Close();
                tabledict.Add("isSuccess", "True");
                return tabledict;
            }
            catch (Exception ex)
            {
                var message = ex.Message;
                Dictionary<string, string> tabledict = new Dictionary<string, string>();
                tabledict.Add("isSuccess", "False");
                tabledict.Add("message", message);
                return tabledict;
            }
        }
        /// <summary>
        /// 获取邮箱参数
        /// </summary>
        /// <param name="domain"></param>
        /// <returns></returns>
        public Dictionary<string, string> SelMailConfig(string domain)
        {
            try
            {
                MySqlConnection mycon = mysqlcon();
                mycon.Open();
                string sql1 = string.Format(@"SELECT * FROM ex_configuration where domain='{0}'", domain);
                MySqlCommand mycmd = new MySqlCommand(sql1, mycon);
                MySqlDataAdapter ada = new MySqlDataAdapter(mycmd);
                DataSet ds = new DataSet();
                ada.Fill(ds, "table");
                Dictionary<string, string> tabledict = new Dictionary<string, string>();
                foreach (DataTable table in ds.Tables)
                {
                    foreach (DataRow row in table.Rows)
                    {
                        foreach (DataColumn column in table.Columns)

                        {
                            tabledict.Add(column.ToString(), row[column].ToString());
                        }
                    }
                }
                mycon.Close();
                tabledict.Add("isSuccess", "True");
                return tabledict;
            }
            catch (Exception ex)
            {
                var message = ex.Message;
                Dictionary<string, string> tabledict = new Dictionary<string, string>();
                tabledict.Add("isSuccess", "False");
                tabledict.Add("message", message);
                return tabledict;
            }
        }


        #endregion

        #region RSA加密算法

        //加密
        public string Encryption1(string express)
        {
            try
            {

                string api = "%$#$";
                string ton = "Admin";
                byte[] plaindata = Encoding.Default.GetBytes(ton + express + api);//将要加密的字符串转换为字节数组
                string Base64Str = Convert.ToBase64String(plaindata);
                //string Base64Str1 = Base64Str.Replace("\n","\\n").Replace("+", "%2B");
                return Base64Str;//将加密后的字节数组转换为字符串
            }
            catch (Exception ex)
            {
                var message = ex.Message;
                return message;
            }
        }

        //解密
        public string Decrypt1(string ciphertext)
        {
            try
            {
                //string ciphertext = ciphertext1.Replace("\\n", "\n").Replace("%2B", "+");
                byte[] encryptdata = Convert.FromBase64String(ciphertext);
                string a = Encoding.Default.GetString(encryptdata);
                string str1 = a.Remove(0, 5);
                string str2 = str1.Remove(str1.Length - 4, 4);
                return str2;

            }
            catch (Exception ex)
            {
                var message = ex.Message;
                return message;
            }

        }


        #endregion
    }
}