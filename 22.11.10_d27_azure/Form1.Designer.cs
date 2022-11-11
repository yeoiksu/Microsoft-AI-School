namespace SQLServer01
{
    partial class frmMain
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.btsConnect = new System.Windows.Forms.Button();
            this.btnGetData = new System.Windows.Forms.Button();
            this.lstBrends = new System.Windows.Forms.ListBox();
            this.gridProducts = new System.Windows.Forms.DataGridView();
            this.btnVIPmembers = new System.Windows.Forms.Button();
            ((System.ComponentModel.ISupportInitialize)(this.gridProducts)).BeginInit();
            this.SuspendLayout();
            // 
            // btsConnect
            // 
            this.btsConnect.Location = new System.Drawing.Point(37, 47);
            this.btsConnect.Name = "btsConnect";
            this.btsConnect.Size = new System.Drawing.Size(141, 33);
            this.btsConnect.TabIndex = 0;
            this.btsConnect.Text = "Connect to Database";
            this.btsConnect.UseVisualStyleBackColor = true;
            this.btsConnect.Click += new System.EventHandler(this.btnConnect_Click);
            // 
            // btnGetData
            // 
            this.btnGetData.Location = new System.Drawing.Point(37, 107);
            this.btnGetData.Name = "btnGetData";
            this.btnGetData.Size = new System.Drawing.Size(141, 35);
            this.btnGetData.TabIndex = 1;
            this.btnGetData.Text = "Get Data";
            this.btnGetData.UseVisualStyleBackColor = true;
            this.btnGetData.Click += new System.EventHandler(this.btnGetData_Click);
            // 
            // lstBrends
            // 
            this.lstBrends.FormattingEnabled = true;
            this.lstBrends.Location = new System.Drawing.Point(195, 47);
            this.lstBrends.Name = "lstBrends";
            this.lstBrends.Size = new System.Drawing.Size(144, 95);
            this.lstBrends.TabIndex = 2;
            this.lstBrends.SelectedIndexChanged += new System.EventHandler(this.lstBrends_SelectedIndexChanged);
            // 
            // gridProducts
            // 
            this.gridProducts.ColumnHeadersHeightSizeMode = System.Windows.Forms.DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            this.gridProducts.Location = new System.Drawing.Point(358, 47);
            this.gridProducts.Name = "gridProducts";
            this.gridProducts.RowHeadersWidth = 51;
            this.gridProducts.Size = new System.Drawing.Size(417, 369);
            this.gridProducts.TabIndex = 3;
            // 
            // btnVIPmembers
            // 
            this.btnVIPmembers.Location = new System.Drawing.Point(37, 167);
            this.btnVIPmembers.Name = "btnVIPmembers";
            this.btnVIPmembers.Size = new System.Drawing.Size(167, 35);
            this.btnVIPmembers.TabIndex = 4;
            this.btnVIPmembers.Text = "VIP Management";
            this.btnVIPmembers.UseVisualStyleBackColor = true;
            this.btnVIPmembers.Click += new System.EventHandler(this.btnVIPmembers_Click);
            // 
            // frmMain
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(800, 450);
            this.Controls.Add(this.btnVIPmembers);
            this.Controls.Add(this.gridProducts);
            this.Controls.Add(this.lstBrends);
            this.Controls.Add(this.btnGetData);
            this.Controls.Add(this.btsConnect);
            this.Name = "frmMain";
            this.Text = "Welcome to SQL Server Tester";
            ((System.ComponentModel.ISupportInitialize)(this.gridProducts)).EndInit();
            this.ResumeLayout(false);

        }

        #endregion

        private System.Windows.Forms.Button btsConnect;
        private System.Windows.Forms.Button btnGetData;
        private System.Windows.Forms.ListBox lstBrends;
        private System.Windows.Forms.DataGridView gridProducts;
        private System.Windows.Forms.Button btnVIPmembers;
    }
}

