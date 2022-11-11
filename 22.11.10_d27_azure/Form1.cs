using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

using System.Data.SqlClient;
using System.Configuration;

namespace SQLServer01
{
    public partial class frmMain : Form
    {
        private string connection_string;
        private SqlConnection SqlCon = null;  // Database 연결
        private SqlCommand SqlCmd = null;     // Command !!
        private SqlDataAdapter SqlApt = new SqlDataAdapter(); // DataAdapter !!

        private DataSet dataMain = new DataSet(); // Dataset !!

        public frmMain()
        {
            InitializeComponent();
        }

        private void btnConnect_Click(object sender, EventArgs e)
        {
            connection_string = ConfigurationManager.AppSettings["connection_string"];
            SqlCon = new SqlConnection(connection_string);  // SQL Databse 연결
            btsConnect.Enabled = false;
        }

        private void btnGetData_Click(object sender, EventArgs e)
        {
            String query = "SELECT * \r\nFROM production.brands";
            SqlCommand cmd = SqlCon.CreateCommand();
            cmd.CommandText = query;
            //cmd.Parameters.Add(new SqlParameter("@id", SqlDbType.Int)).Value = 5;

            SqlApt.SelectCommand = cmd;
            SqlApt.Fill(dataMain);  // Data를 가져와서 dataMain에 추가

            lstBrends.Items.Clear();  // 먼저 clear하고 시작해야함 !!

            DataRowCollection dataRows = dataMain.Tables[0].Rows;  // collection 열들이 묶여져있는 것

            for(int i = 0; i < dataRows.Count; i++)
            {
                lstBrends.Items.Add(dataRows[i][1].ToString());  // 
            }

            btnGetData.Enabled = false;

        }

        private void lstBrends_SelectedIndexChanged(object sender, EventArgs e)
        {
            if(lstBrends.SelectedIndex == -1)  // 선택한게 없다면
            {
                return;
            }

            // Fill to DataGridView
            int selectedIndex = lstBrends.SelectedIndex;  // 선택받은 index
            int selectedBrandID = Int32.Parse(dataMain.Tables[0].Rows[selectedIndex][0].ToString());  // 원하는 row 선택

            DataSet dataProducts = new DataSet();
            string query = "SELECT * FROM production.products WHERE brand_id = @brand_id";
            SqlCommand cmd = SqlCon.CreateCommand();
            cmd.Parameters.Add(new SqlParameter("@brand_id", SqlDbType.Int)).Value = selectedBrandID;
            cmd.CommandText = query;

            SqlApt.SelectCommand = cmd;
            SqlApt.Fill(dataProducts);  // Data를 가져워솨 dataProducts에 추가
            gridProducts.DataSource = dataProducts.Tables[0];  // Binding
        }

        private void btnVIPmembers_Click(object sender, EventArgs e)  // button 클릭 시, 다른 form(다른 class)으로 이동
        {
            frmVIPMembers vip = new frmVIPMembers();
            vip.ShowDialog();
        }
    }
}
