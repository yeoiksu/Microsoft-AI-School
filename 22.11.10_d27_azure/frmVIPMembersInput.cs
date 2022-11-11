using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

using System.Configuration;
using System.Data.SqlClient;

namespace SQLServer01
{
    public partial class frmVIPMembersInput : Form
    {
        private string connection_string;
        private frmVIPMembers frm_vip_members;


        public frmVIPMembersInput(frmVIPMembers vip_members)
        {
            InitializeComponent();
            frm_vip_members = vip_members;
        }

        private void frmVIPMembersInput_Load(object sender, EventArgs e)
        {

        }
        private void btnOK_Click(object sender, EventArgs e)
        {
            if (txtName.Text.Trim().Length == 0)     // Name textbox이 NULL이라면, Trim(): 공백 제거 함수
            {
                MessageBox.Show("Please input VIP Name! : ",    // message
                    "ERROR",   // captiion
                    MessageBoxButtons.OK,   // button type
                    MessageBoxIcon.Error);
                return;
            }

            // Database에 입력하는 부분 !!!
            connection_string = ConfigurationManager.AppSettings["connection_string"];
            string query = "INSERT INTO dbo.VIPmembers(member_name, member_email, member_phone) VALUES('@name', '@email', '@phone')";

            SqlConnection con = new SqlConnection(connection_string);  // 연결
            SqlCommand cmd = con.CreateCommand();

            cmd.CommandText = query;
            cmd.Parameters.Add(new SqlParameter("@name", SqlDbType.VarChar, 200)).Value = txtName.Text;
            cmd.Parameters.Add(new SqlParameter("@email", SqlDbType.VarChar, 100)).Value = txtEmail.Text;
            cmd.Parameters.Add(new SqlParameter("@phone", SqlDbType.VarChar, 25)).Value = txtPhone.Text;

            con.Open();
            cmd.ExecuteNonQuery();  // 입력
            con.Close();

            frm_vip_members.ReloadData();  // 입력이 끝난 후 frmVIPMembers.cs >> Reload() 함수 호출되면서 초기화

            this.Close();

        }

        private void btnCancel_Click(object sender, EventArgs e)
        {
            if (txtName.Text.Trim().Length != 0)  // Name textbox이 NULL이 아니라면, Trim(): 공백 제거 함수
            {
                var buttonResult = 
                    MessageBox.Show("Close right now ?",
                    "Close",
                    MessageBoxButtons.YesNo,
                    MessageBoxIcon.Warning);  // yes no 

                if(buttonResult == DialogResult.No) // no라면 계속 진행, DialogResult를 통해 위의 결과를 가져옴
                {
                    return;
                }
            }  
            this.Close();  // yes라면 진행 종료
        }
    }
}
