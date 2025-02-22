
import customtkinter
import tkinter
from tkinter import ttk
import datetime
import csv
import re
import pandas as pd
from tkcalendar import Calendar
from operations import Operations
import matplotlib.pyplot as plt
import sqlite3
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

ops=Operations()

def staff_work(un):
  empcode=un
  # important note
  def important_note():
    tkinter.messagebox.showinfo("Information","*-->When same clients are available then check if  projects are different \n if different click YES otherwise NO")
  # clearing the trees
  def clear():
    for records in treev_total_data.get_children():
      treev_total_data.delete(records)
    for records in treev_today.get_children():
      treev_today.delete(records)
    for records in treev_tomorrow.get_children():
      treev_tomorrow.delete(records)
  
  # data entry function
  def Submit():
    global end_date_flag
    
    project_id=pid.get().strip()
    project_title=pname.get().strip()
    client_name=cname.get().strip()
    client_phone=cphone.get().strip()
    client_email=cemail.get().strip()
    text=textbox.get("1.0","end-1c").strip()
    fees=fee.get().strip()
    
    
    ans=tkinter.messagebox.askyesno("Add Project","Are you sure you want to add this project\n Check the details carefully",icon="warning")
    
    if ans:
      # CHECKING IF DETAILS ARE THERE OR NOT
      data123=[project_id,project_title,client_name,client_phone,client_email,text,fees]
      for i in data123:
        if i=="" or i==" ":
          submit_status.configure(text="error-fill all fields",font=font)
          return
        
      data123=[fees,client_phone]
      for i in data123:
        for j in i:
          if j in [str(a) for a in range(0,10)] or j in ["."]:
            pass
          else:
            submit_status.configure(text="error-number field",font=font)
            return
      
      if(len(client_phone)!=10):
        submit_status.configure(text="error-phone",font=font)
        return
      
      
      data123=[client_email]
      pattern=r"^[\d a-z]?\w+[\.]?\w+@+\w+\.+\w+[\.]?\w+"
      for i in data123:
        if re.match(pattern,i):
          pass
        else:
          submit_status.configure(text="error-emails",font=font)
          return
        
      if end_date_flag==1:
        submit_status.configure(text="error-set deadline",font=font)
        return
      else:
          end=str(cal.get_date().strip())
     
      # WRITING
      
      project_to_be_added={
      "id":project_id,
      "name":project_title,
      "client_name":client_name,
      "client_phone":client_phone,
      "client_email":client_email,
      "description":text,
      "end_date":datetime.datetime.strptime(end, "%m/%d/%y").strftime("%Y/%m/%d"),
      "commission":float(fees),
      "employee_id":un
      }
      
      ops.insert_project(project_to_be_added)
     
      # CLEANING THE ENTRY FIELDS
      widgets=[pid,pname,cname,cphone,cemail,fee]
      for i in widgets:
        i.delete(0,"end")
        
      textbox.delete("1.0","end-1c")#to empty the text box
      
      end_date.configure(text="MM/DD/YYYY")
      # UPDATING THE LABEL
      submit_status.configure(text="ADDED")
      end_date_flag=1
      show_data()
  
  #date picker
  def date_picker():
    global cal
    cal_root=customtkinter.CTk()
    cal_root.title("Choose deadline date")
    cal_root.geometry("300x300")
    cal = Calendar(cal_root, selectmode = 'day',
                 year = int(datetime.datetime.now().strftime("%y")),
                 month = int(datetime.datetime.now().strftime("%m")),
                 day = int(datetime.datetime.now().strftime("%d")))
    cal.pack()
    def date_ok():
      global end_date_flag
      end_date.configure(text=f"{cal.get_date()}")
      end_date_flag=0
      cal_root.destroy()
    customtkinter.CTkButton(cal_root,text="ok",command=date_ok).pack()
    cal_root.mainloop()
  
  # displaying data
  def show_data():
    data = ops.get_all_projects_undone(un)
    try:
      clear()
    except:
      None
    columns=['Project id','Project','Client Name','Client Phone','Client Email','Description','Start Date','End Date','Commission','Freelancer Commission','Status','Employee id','Freelancer id']
    treev_total_data["columns"] = columns
    for col in columns:  
      treev_total_data.heading(col, text=col, anchor="center")  # Set column heading
    for row in data:  
      treev_total_data.insert("", "end", values=row)
    total_projects_label_pending.configure(text=f"{len(data)}")
    
    treev_today["columns"] = columns
    for col in columns:  
      treev_today.heading(col, text=col, anchor="center")  # Set column heading
    for row in data:  
      treev_today.insert("", "end", values=row)
    total_projects_label_today.configure(text=f"{len(data)}")
    
    treev_tomorrow["columns"] = columns
    for col in columns:  
      treev_tomorrow.heading(col, text=col, anchor="center")  # Set column heading
    for row in data:  
      treev_tomorrow.insert("", "end", values=row)
    total_projects_label_tomorrow.configure(text=f"{len(data)}")
    
    treev_late["columns"] = columns
    for col in columns:  
      treev_late.heading(col, text=col, anchor="center")  # Set column heading
    for row in data:  
      treev_late.insert("", "end", values=row)
    total_projects_label_late.configure(text=f"{len(data)}")
  
  # deleting one Resource
  def delete_one():
    global data
    ans=tkinter.messagebox.askyesno("Task done","Are you sure this task is done be sure",icon="warning")
    if ans:
      grabbed=treev_total_data.focus()#to get the data of the row selected
      values=treev_total_data.item(grabbed,"values")
      selection=treev_total_data.selection()#to get the selected the row
      treev_total_data.delete(selection)
      data.loc[(data["CLIENT NAME"]==values[0])&(data["CLIENT EMAIL"]==values[1])&(data["PROJECT"]==values[2])&((data["FEE"]==int(values[3])) | (data["FEE"]==float(values[3])))&(data["FREELANCER"]==values[4])&((data["COMMISSION"]==int(values[5]))|(data["COMMISSION"]==float(values[5])))&(data["FREELANCER EMAIL"]==values[6])&(data["START"]==values[7])&(data["END"]==values[8])&(data["EMP ID"]==values[9])&(data["STATUS"]==1),"STATUS"]=0
      data.to_csv("data.csv",index=False)
      data=pd.read_csv("data.csv")
      show_data()
      from_staff_emp_data=pd.read_csv("emp_dropse_data.csv")
      from_staff_emp_data.loc[(from_staff_emp_data["USERNAME"]==empcode),"DONE"]+=1
      from_staff_emp_data.to_csv("emp_dropse_data.csv",index=False)
    
  # deleting multiple
  def delete_all():
    global data
    ans=tkinter.messagebox.askyesno("All task done","Are you sure that all these tasksare done",icon="warning")
    if ans:
      data.loc[(data["EMP ID"]==empcode)&(data["STATUS"]==1),"STATUS"]=0
      from_staff_emp_data=pd.read_csv("emp_dropse_data.csv")
      from_staff_emp_data.loc[(from_staff_emp_data["USERNAME"]==empcode),"DONE"]+=len(treev_total_data.get_children())
      from_staff_emp_data.to_csv("emp_dropse_data.csv",index=False)
      for records in treev_total_data.get_children():
        treev_total_data.delete(records)
      data.to_csv("data.csv",index=False)
      data=pd.read_csv("data.csv")
      show_data()
  
  # closing the window
  def confirm():
    ans=tkinter.messagebox.askyesno("exit","Are you sure you want to LOGOUT",icon="warning")
    if ans:
      root.destroy()
  
  # changing the password
  def change_pw():
    def change():
      old_password=old_pw.get()
      new_password=new_pw.get()
      from_staff_emp_data=pd.read_csv("emp_dropse_data.csv")
      pw_check_data=from_staff_emp_data.loc[(from_staff_emp_data["PASSWORD"]==old_password)&(from_staff_emp_data["USERNAME"]==empcode)]
      if pw_check_data.empty:
        tkinter.messagebox.showerror("Password not matched","old password not matched")
        old_pw.delete(0,"end")
      else:
        from_staff_emp_data.loc[(from_staff_emp_data["PASSWORD"]==old_password)&(from_staff_emp_data["USERNAME"]==empcode),"PASSWORD"]=new_password
        from_staff_emp_data.to_csv("emp_dropse_data.csv",index=False)
        pw_root.destroy()
        tkinter.messagebox.showinfo("changed","password changed")
    pw_root=customtkinter.CTk()
    pw_root.title("change password")
    pw_root.geometry("280x200")
    pw_root.configure(padx=10,pady=10)
    pw_root.resizable(False,False)
    pw_frame=customtkinter.CTkFrame(pw_root)
    pw_frame.place(relheight=1,relwidth=1)
    old_pw=customtkinter.CTkEntry(pw_frame,placeholder_text="write old password",show="*",width=240)
    old_pw.grid(row=0, column=0,padx=(5, 0), pady=(5, 5))
    new_pw=customtkinter.CTkEntry(pw_frame,placeholder_text="write new password",show="*",width=240)
    new_pw.grid(row=1, column=0,padx=(5, 0), pady=(5, 5))
    customtkinter.CTkButton(pw_frame,text="Change",font=font,command=change).grid(row=2,column=0,padx=(5, 0), pady=(5, 5))
  
  # analytics page
  def analytics():
    # Connect to SQLite database
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Fetch projects per employee
    cursor.execute("SELECT employee_id, COUNT(*) FROM projects GROUP BY employee_id")
    projects_per_employee = cursor.fetchall()

    # Fetch project completion status
    cursor.execute("SELECT status, COUNT(*) FROM projects GROUP BY status")
    project_status = cursor.fetchall()

    # Fetch earnings per project
    cursor.execute("SELECT id, commission FROM projects")
    earnings_per_project = cursor.fetchall()

    # Fetch commission distribution (Total vs. Freelancer)
    cursor.execute("SELECT id, commission, freelancer_commission FROM projects")
    commission_distribution = cursor.fetchall()

    conn.close()  # Close the database connection

    # Create figure for multiple plots
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    fig.suptitle("Project Analytics", fontsize=14, fontweight="bold")
    fig.tight_layout(pad=5.0)

    ### 1️⃣ **Projects per Employee (Bar Chart)**
    if projects_per_employee:
        employee_ids = [str(row[0]) for row in projects_per_employee]
        project_counts = [row[1] for row in projects_per_employee]
        
        axes[0, 0].bar(employee_ids, project_counts, color="blue")
        axes[0, 0].set_title("Projects per Employee", fontsize=12)
        axes[0, 0].set_xlabel("Employee ID")
        axes[0, 0].set_ylabel("Number of Projects")
        axes[0, 0].tick_params(axis="x", rotation=30)

    ### 2️⃣ **Project Completion Status (Pie Chart)**
    # if project_status:
    #     labels = ["Completed", "Ongoing"]
    #     counts = [row[1] for row in project_status]

    #     axes[0, 1].pie(counts, labels=labels, autopct='%1.1f%%', colors=["green", "red"], startangle=140)
    #     axes[0, 1].set_title("Project Completion Status", fontsize=12)

    ### 3️⃣ **Earnings per Project (Bar Chart)**
    if earnings_per_project:
        project_ids = [str(row[0]) for row in earnings_per_project]
        commissions = [row[1] for row in earnings_per_project]

        axes[1, 0].bar(project_ids, commissions, color="purple")
        axes[1, 0].set_title("Earnings per Project", fontsize=12)
        axes[1, 0].set_xlabel("Project ID")
        axes[1, 0].set_ylabel("Commission Earned")
        axes[1, 0].tick_params(axis="x", rotation=30)

    ### 4️⃣ **Employee vs. Freelancer Commission (Stacked Bar Chart)**
    if commission_distribution:
        project_ids = [str(row[0]) for row in commission_distribution]
        total_commissions = [row[1] for row in commission_distribution]
        freelancer_commissions = [row[2] if row[2] is not None else 0 for row in commission_distribution]
        employee_commissions = [total - freelancer for total, freelancer in zip(total_commissions, freelancer_commissions)]

        axes[1, 1].bar(project_ids, employee_commissions, label="Employee", color="blue")
        axes[1, 1].bar(project_ids, freelancer_commissions, label="Freelancer", color="orange", bottom=employee_commissions)
        axes[1, 1].set_title("Commission Distribution", fontsize=12)
        axes[1, 1].set_xlabel("Project ID")
        axes[1, 1].set_ylabel("Commission Amount")
        axes[1, 1].legend()
        axes[1, 1].tick_params(axis="x", rotation=30)

    # Adjust layout
    plt.tight_layout()

    # Embed the figure in Tkinter
    for widget in left_tabs.tab("Analytics").winfo_children():
        widget.destroy()  # Clear previous graphs before adding a new one

    canvas = FigureCanvasTkAgg(fig, master=left_tabs.tab("Analytics"))
    canvas.draw()
    canvas.get_tk_widget().grid(row=1, column=0, padx=20, pady=20)
  
  # making the root
  customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
  customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"
  
  root=customtkinter.CTk()
  root.title("OutSourcery")
  Width= root.winfo_screenwidth()#
  Height= root.winfo_screenheight()# both doe
  root.geometry("%dx%d" % (Width, Height))
  root.config(padx=10,pady=10)
  font=("Times New Roman",20,"bold")
  
  # Create a style object
  style = ttk.Style()
  style.configure("Treeview", font=("Times New Roman", 18),rowheight=40)  # Change font size
  style.configure("Treeview.Heading", font=("Times New Roman", 20, "bold"),rowheight=40)  # Change heading font size

  # making the frames
  top_frame = tkinter.Frame(root,bg="#333333")
  top_frame.place(relwidth=1,height=100)
  
  left_tabs = customtkinter.CTkTabview(root)
  left_tabs.place(relx=0,rely=0.12,relwidth=0.52,relheight=0.88)
  
  left_tabs.add("Total Data")
  left_tabs.add("Analytics")
  
  total_data_frame = customtkinter.CTkFrame(left_tabs.tab("Total Data"))
  total_data_frame.place(relx=0,rely=0,relwidth=1,relheight=1)
  
  customtkinter.CTkButton(left_tabs.tab("Analytics"),command=analytics,text="Gain Analytics").grid(row=0,column=1)
  
  right_tabs = customtkinter.CTkTabview(root)
  right_tabs.place(relx=0.53,rely=0.12,relwidth=0.47,relheight=0.88)
  
  right_tabs.add("Home")
  right_tabs.add("Today")
  right_tabs.add("Tomorrow")
  right_tabs.add("Late")
  right_tabs.add("Freelancers")
  right_tabs.add("Add Project")
  
  today_frame=customtkinter.CTkFrame(right_tabs.tab("Today"))# CAN BE making a tab scrollable
  today_frame.place(relheight=1,relwidth=1)
  
  tomorrow_frame=customtkinter.CTkFrame(right_tabs.tab("Tomorrow"))# CAN BE making a tab scrollable
  tomorrow_frame.place(relheight=1,relwidth=1)
  
  late_frame=customtkinter.CTkFrame(right_tabs.tab("Late"))# CAN BE making a tab scrollable
  late_frame.place(relheight=1,relwidth=1)
  # top frame
  top_frame.configure(padx=2,pady=2)
  customtkinter.CTkLabel(top_frame,text="OutSourcery",font=font).grid(row=0,column=0,padx=20, pady=0)
  customtkinter.CTkButton(top_frame,text="Task completed",font=font,command=delete_one).grid(row=0,column=2,padx=20, pady=10)
  customtkinter.CTkButton(top_frame,text="All Task completed",font=font,command=delete_all).grid(row=0,column=3,padx=20, pady=10)
  customtkinter.CTkButton(top_frame,text="Important note",font=font,command=important_note).grid(row=0,column=4,padx=20, pady=10)
  customtkinter.CTkButton(top_frame,text="Change password",font=font,command=change_pw).grid(row=0,column=5,padx=20, pady=10)
  
  #namaskar
  customtkinter.CTkLabel(right_tabs.tab("Home"),text=empcode,font=font).grid(row=0,column=0,padx=20, pady=10)
  customtkinter.CTkLabel(right_tabs.tab("Home"),text="total projects pending",font=font).grid(row=1,column=0,padx=20, pady=10)
  customtkinter.CTkLabel(right_tabs.tab("Home"),text="total projects for today",font=font).grid(row=2,column=0,padx=20, pady=10)
  customtkinter.CTkLabel(right_tabs.tab("Home"),text="total projects for tomorrow",font=font).grid(row=3,column=0,padx=20, pady=10)
  customtkinter.CTkLabel(right_tabs.tab("Home"),text="total late projects",font=font).grid(row=4,column=0,padx=20, pady=10)
  total_projects_label_pending=customtkinter.CTkLabel(right_tabs.tab("Home"),text="",font=font)
  total_projects_label_pending.grid(row=1,column=1,padx=20, pady=10)
  total_projects_label_tomorrow=customtkinter.CTkLabel(right_tabs.tab("Home"),text="",font=font)
  total_projects_label_tomorrow.grid(row=3,column=1,padx=20, pady=10)
  total_projects_label_today=customtkinter.CTkLabel(right_tabs.tab("Home"),text="",font=font)
  total_projects_label_today.grid(row=2,column=1,padx=20, pady=10)
  total_projects_label_late=customtkinter.CTkLabel(right_tabs.tab("Home"),text="",font=font)
  total_projects_label_late.grid(row=4,column=1,padx=20, pady=10)
  
  
  #add project
  
  customtkinter.CTkLabel(right_tabs.tab("Add Project"),text="project id",font=font).grid(row=0,column=0)
  pid = customtkinter.CTkEntry(right_tabs.tab("Add Project"), placeholder_text="project id",width=240)
  pid.grid(row=0, column=1,padx=(5, 0), pady=(5, 5))
  
  customtkinter.CTkLabel(right_tabs.tab("Add Project"),text="project name",font=font).grid(row=1,column=0)
  pname = customtkinter.CTkEntry(right_tabs.tab("Add Project"), placeholder_text="project name",width=240)
  pname.grid(row=1, column=1,padx=(5, 0), pady=(5, 5))
  
  customtkinter.CTkLabel(right_tabs.tab("Add Project"),text="client name",font=font).grid(row=2,column=0)
  cname = customtkinter.CTkEntry(right_tabs.tab("Add Project"), placeholder_text="client name",width=240)
  cname.grid(row=2, column=1,padx=(5, 0), pady=(5, 5))
  
  customtkinter.CTkLabel(right_tabs.tab("Add Project"),text="client phone",font=font).grid(row=3,column=0)
  cphone = customtkinter.CTkEntry(right_tabs.tab("Add Project"), placeholder_text="client phone",width=240)
  cphone.grid(row=3, column=1,padx=(5, 0), pady=(5, 5))
  
  customtkinter.CTkLabel(right_tabs.tab("Add Project"),text="client email",font=font).grid(row=4,column=0)
  cemail = customtkinter.CTkEntry(right_tabs.tab("Add Project"), placeholder_text="client email",width=240)
  cemail.grid(row=4, column=1,padx=(5, 0), pady=(5, 5))
  
  customtkinter.CTkLabel(right_tabs.tab("Add Project"),text="project",font=font).grid(row=5,column=0)
  textbox = customtkinter.CTkTextbox(right_tabs.tab("Add Project"), width=250,height=100)
  textbox.grid(row=5, column=1, padx=(20, 0), pady=(20, 0))
  
  customtkinter.CTkLabel(right_tabs.tab("Add Project"),text="fee $",font=font).grid(row=6,column=0)
  fee = customtkinter.CTkEntry(right_tabs.tab("Add Project"), placeholder_text="fee",width=240)
  fee.grid(row=6, column=1,padx=(5, 0), pady=(5, 5))
  
  end_date_flag=1
  customtkinter.CTkLabel(right_tabs.tab("Add Project"),text="deadline end",font=font).grid(row=7,column=0)
  end_date=customtkinter.CTkLabel(right_tabs.tab("Add Project"),text="YYYY-MM-DD",font=font)
  end_date.grid(row=7,column=1)
  customtkinter.CTkButton(right_tabs.tab("Add Project"),command=date_picker,text="Pick Date").grid(row=7,column=2)
  
  customtkinter.CTkButton(right_tabs.tab("Add Project"),command=Submit,text="Submit").grid(row=8,column=1)
  submit_status=customtkinter.CTkLabel(right_tabs.tab("Add Project"),text="",font=font)
  submit_status.grid(row=9,column=1)
  
  
  # total data frame
  treev_total_data = tkinter.ttk.Treeview(total_data_frame, selectmode ='browse')#extended helps to select multiple and none to none
  treev_total_data.place(relheight=1, relwidth=1)
  
  treescrolly = tkinter.Scrollbar(total_data_frame, orient="vertical", command=treev_total_data.yview) # command means update the yaxis view of the widget
  treescrollx = tkinter.Scrollbar(total_data_frame, orient="horizontal", command=treev_total_data.xview) # command means update the xaxis view of the widget
  treev_total_data.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set) # assign the scrollbars to the Treeview Widget
  treescrollx.pack(side="bottom", fill="x") # make the scrollbar fill the x axis of the Treeview widget
  treescrolly.pack(side="right", fill="y") # make the scrollbar fill the y axis of the Treeview widget
    
  # today_frame
  treev_today = tkinter.ttk.Treeview(today_frame, selectmode ='browse')#extended helps to select multiple and none to none
  treev_today.place(relheight=1, relwidth=1)
  
  treescrolly = tkinter.Scrollbar(today_frame, orient="vertical", command=treev_today.yview) # command means update the yaxis view of the widget
  treescrollx = tkinter.Scrollbar(today_frame, orient="horizontal", command=treev_today.xview) # command means update the xaxis view of the widget
  treev_today.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set) # assign the scrollbars to the Treeview Widget
  treescrollx.pack(side="bottom", fill="x") # make the scrollbar fill the x axis of the Treeview widget
  treescrolly.pack(side="right", fill="y") # make the scrollbar fill the y axis of the Treeview widget
  # tomorrow_frame
  treev_tomorrow = tkinter.ttk.Treeview(tomorrow_frame, selectmode ='browse')#extended helps to select multiple and none to none
  treev_tomorrow.place(relheight=1, relwidth=1)
  
  treescrolly = tkinter.Scrollbar(tomorrow_frame, orient="vertical", command=treev_tomorrow.yview) # command means update the yaxis view of the widget
  treescrollx = tkinter.Scrollbar(tomorrow_frame, orient="horizontal", command=treev_tomorrow.xview) # command means update the xaxis view of the widget
  treev_tomorrow.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set) # assign the scrollbars to the Treeview Widget
  treescrollx.pack(side="bottom", fill="x") # make the scrollbar fill the x axis of the Treeview widget
  treescrolly.pack(side="right", fill="y") # make the scrollbar fill the y axis of the Treeview widget
  # late_frame
  treev_late = tkinter.ttk.Treeview(late_frame, selectmode ='browse')#extended helps to select multiple and none to none
  treev_late.place(relheight=1, relwidth=1)
  
  treescrolly = tkinter.Scrollbar(late_frame, orient="vertical", command=treev_late.yview) # command means update the yaxis view of the widget
  treescrollx = tkinter.Scrollbar(late_frame, orient="horizontal", command=treev_late.xview) # command means update the xaxis view of the widget
  treev_late.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set) # assign the scrollbars to the Treeview Widget
  treescrollx.pack(side="bottom", fill="x") # make the scrollbar fill the x axis of the Treeview widget
  treescrolly.pack(side="right", fill="y") # make the scrollbar fill the y axis of the Treeview widget
  # styling the tree view
  style = tkinter.ttk.Style(root)
  style.configure("Treeview", background="#333333", fieldbackground="#333333", foreground="white")
  
  style.map('Treeview',background=[('selected',"red")])#to change the color of selected
 
  show_data()
  
  root.protocol("WM_DELETE_WINDOW",confirm)
  root.mainloop()

if __name__=="__main__":
  staff_work('E001')
