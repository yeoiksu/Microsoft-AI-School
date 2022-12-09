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
    public partial class frmVIPMembers : Form
    {
        private string connection_string = "";
        private SqlConnection SqlCon = null;  // Database 연결
        private SqlCommand SqlCmd = null;     // Command !!
        private SqlDataAdapter SqlApt = new SqlDataAdapter(); // DataAdapter !!

        private DataSet dataMain = new DataSet(); // Dataset !!

        public frmVIPMembers()
        {
            InitializeComponent();  // 제일 처음에 생성될 때 : 생성자
        }

        private void btnClose_Click(object sender, EventArgs e)  // 클릭 시, 창이 close
        {
            this.Close();  // 종료
        }

        private void frmVIPMembers_Load(object sender, EventArgs e)  // form이 loading 될 때 event
        {
            connection_string = ConfigurationManager.AppSettings["connection_string"];
            ReloadData();
        }

        public void ReloadData()  // public
        {   
            dataMain.Clear();   

            SqlCon = new SqlConnection(connection_string);  // SQL Databse 연결

            String query = "SELECT * FROM dbo.VIPmembers";
            SqlCommand cmd = SqlCon.CreateCommand();
            cmd.CommandText = query;

            SqlApt.SelectCommand = cmd;
            SqlApt.Fill(dataMain);  // Data를 가져와서 dataMain에 추가

            grdMemberList.DataSource = dataMain.Tables[0];  // 먼저 clear하고 시작해야함 !!
        }

        private void btnAdd_Click(object sender, EventArgs e)
        {
            frmVIPMembersInput vipInput = new frmVIPMembersInput(this);  // this 현재 자기 form을 주면서 자기자신 호출
                                                                         // frmVIPMembersInput.cs 생성자 부분 수정 필요 !! 
            vipInput.ShowDialog();
        }
    }
}
