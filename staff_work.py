
import tkinter.messagebox
import customtkinter
import tkinter
from tkinter import ttk
import datetime
import re
from tkcalendar import Calendar
from operations import Operations

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
    for records in treev_freelancer.get_children():
      treev_freelancer.delete(records)
  
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
      "end_date":datetime.datetime.strptime(end, "%m/%d/%y").strftime("%Y-%m-%d"),
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
      end_date.configure(text=f"{datetime.datetime.strptime(cal.get_date(), '%m/%d/%y').strftime('%Y-%m-%d')}")
      end_date_flag=0
      cal_root.destroy()
    customtkinter.CTkButton(cal_root,text="ok",command=date_ok).pack()
    cal_root.mainloop()
  
  # displaying data
  def show_data():
    data = ops.get_all_projects_undone(un)
    data_today=ops.get_all_projects_undone_today(un)
    data_tomorrow=ops.get_all_projects_undone_tomorrow(un)
    data_late=ops.get_all_projects_undone_late(un)
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
    for row in data_today:  
      treev_today.insert("", "end", values=row)
    total_projects_label_today.configure(text=f"{len(data_today)}")
    
    treev_tomorrow["columns"] = columns
    for col in columns:  
      treev_tomorrow.heading(col, text=col, anchor="center")  # Set column heading
    for row in data_tomorrow:  
      treev_tomorrow.insert("", "end", values=row)
    total_projects_label_tomorrow.configure(text=f"{len(data_tomorrow)}")
    
    treev_late["columns"] = columns
    for col in columns:  
      treev_late.heading(col, text=col, anchor="center")  # Set column heading
    for row in data_late:  
      treev_late.insert("", "end", values=row)
    total_projects_label_late.configure(text=f"{len(data_late)}")
     
    columns_freelancer=['Freelancer id','Freelancer Name','Freelancer Phone','Freelancer Email','Project Assigned','Currently Available','Projects Completed']
    treev_freelancer["columns"] = columns_freelancer
    for col in columns_freelancer:  
      treev_freelancer.heading(col, text=col, anchor="center")  # Set column heading
    freelancers=ops.get_all_freelancers()
    for row in freelancers:  
      treev_freelancer.insert("", "end", values=row)
  
    
  # deleting multiple
  def delete():
    ans=tkinter.messagebox.askyesno("All task done","Are you sure that all these tasksare done",icon="warning")
    if ans:
      grabbed=treev_total_data.focus()
      values=treev_total_data.item(grabbed,"values")
      selection=treev_total_data.selection()
      if values and values[-1]=='None':
        tkinter.messagebox.showerror("Warning","Can't complete unassigned project")
      elif values:
        ops.update_project_status(values[0],1)
        ops.update_completion_freelancer_emp_status(values[-1],values[-2])
        treev_total_data.delete(selection)
        tkinter.messagebox.showinfo("Project","project completed")
      else:
        tkinter.messagebox.showerror("Project","Select a project")
      show_data()

  # assign project
  def Assign_project():
    def assign():
      freelancer_commission=freelance_comm.get().strip()
      freelancer_id=freelance_id.get().strip()

      grabbed=treev_total_data.focus()
      values=treev_total_data.item(grabbed,"values")

      freelancer_data=ops.get_freelancer_data(freelancer_id)
      print(freelancer_data)

      if freelancer_data[0][0]:
        if values and values[-1]!='None':
          ans=tkinter.messagebox.askyesno("Re-Assign Project",f"Would you like to re assign project from {values[-1]} to {freelancer_id} ",icon="warning")
          if ans:
            ops.assign_project(values[0],freelancer_id,float(freelancer_commission),values[0]+"---"+values[1])
            ap_root.destroy()
            tkinter.messagebox.showinfo("Project","Project Re-Assigned")
          else:
            ap_root.destroy()
            tkinter.messagebox.showerror("Project","Project Not Assigned")
        elif values:
          ops.assign_project(values[0],freelancer_id,float(freelancer_commission),values[0]+"---"+values[1])
          ap_root.destroy()
          tkinter.messagebox.showinfo("Project","Project Assigned")
        else:
          ap_root.destroy()
          tkinter.messagebox.showerror("Project","Select a Project")
      else:
        ap_root.destroy()
        tkinter.messagebox.showerror("Project","Freelancer not available")
      show_data()

    
    ap_root=customtkinter.CTkToplevel()
    ap_root.title("Assign Project")
    ap_root.geometry("280x200")
    ap_root.configure(padx=10,pady=10)
    ap_root.resizable(False,False)
    ap_frame=customtkinter.CTkFrame(ap_root)
    ap_frame.place(relheight=1,relwidth=1)
    freelance_comm=customtkinter.CTkEntry(ap_frame,placeholder_text="freelancer commission",width=240)
    freelance_comm.grid(row=0, column=0,padx=(5, 0), pady=(5, 5))
    freelance_id=customtkinter.CTkEntry(ap_frame,placeholder_text="freelancer id",width=240)
    freelance_id.grid(row=1, column=0,padx=(5, 0), pady=(5, 5))
    customtkinter.CTkButton(ap_frame,text="Assign",font=font,command=assign).grid(row=2,column=0,padx=(5, 0), pady=(5, 5))

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
      pw_check_data=ops.check_password(un,old_password)
      if not pw_check_data:
        tkinter.messagebox.showerror("Password not matched","old password not matched")
        old_pw.delete(0,"end")
      else:
        ops.change_password(un,new_password)
        pw_root.destroy()
        tkinter.messagebox.showinfo("changed","password changed")
    pw_root=customtkinter.CTkToplevel()
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
  
  # adding freelancer
  def AddFreelancer():
    freelancer_id=free_id.get().strip()
    freelancer_name=free_name.get().strip()
    freelancer_email=free_email.get().strip()
    freelancer_phone=free_phone.get().strip()
    ans=tkinter.messagebox.askyesno("Add Freelancer","Are you sure you want to add this freelancer\n Check the details carefully",icon="warning")
    data123=[freelancer_name,freelancer_id,freelancer_email,freelancer_phone]
    for i in data123:
      if i=="" or i==" ":
        free_submit_status.configure(text="error-fill all fields",font=font)
        return
      
    data123=[freelancer_email]
    pattern=r"^[\d a-z]?\w+[\.]?\w+@+\w+\.+\w+[\.]?\w+"
    for i in data123:
      if re.match(pattern,i):
        pass
      else:
        free_submit_status.configure(text="error-emails",font=font)
        return
      
    if(len(freelancer_phone)!=10):
      free_submit_status.configure(text="error-phone",font=font)
      return
    
    
    for j in freelancer_phone:
      if j in [str(a) for a in range(0,10)] or j in ["."]:
        pass
      else:
        free_submit_status.configure(text="error-number field",font=font)
        return
      
    freelancer_to_be_added={
    "id":freelancer_id,
    "name":freelancer_name,
    "phone":freelancer_phone,
    "email":freelancer_email
    }
    ops.insert_freelancer(freelancer_to_be_added)

    widgets=[free_id,free_name,free_email,free_phone] 
    for i in widgets:
      i.delete(0,"end")
    free_submit_status.configure(text="ADDED")
    show_data()


  # analytics page
  def analytics():
    ...
  
  
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
  left_tabs.add("Add Freelancer")


  
  total_data_frame = customtkinter.CTkFrame(left_tabs.tab("Total Data"))
  total_data_frame.place(relx=0,rely=0,relwidth=1,relheight=1)
  
  customtkinter.CTkButton(left_tabs.tab("Analytics"),command=analytics,text="Gain Analytics").grid(row=0,column=1)

  # making the add freelancer tab

  customtkinter.CTkLabel(left_tabs.tab("Add Freelancer"),text="freelancer id",font=font).grid(row=0,column=0)
  free_id = customtkinter.CTkEntry(left_tabs.tab("Add Freelancer"), placeholder_text="freelancer id",width=240)
  free_id.grid(row=0, column=1,padx=(5, 0), pady=(5, 5))
  
  customtkinter.CTkLabel(left_tabs.tab("Add Freelancer"),text="freelancer name",font=font).grid(row=1,column=0)
  free_name = customtkinter.CTkEntry(left_tabs.tab("Add Freelancer"), placeholder_text="freelancer name",width=240)
  free_name.grid(row=1, column=1,padx=(5, 0), pady=(5, 5))
  
  customtkinter.CTkLabel(left_tabs.tab("Add Freelancer"),text="freelancer email",font=font).grid(row=2,column=0)
  free_email = customtkinter.CTkEntry(left_tabs.tab("Add Freelancer"), placeholder_text="freelancer email",width=240)
  free_email.grid(row=2, column=1,padx=(5, 0), pady=(5, 5))
  
  customtkinter.CTkLabel(left_tabs.tab("Add Freelancer"),text="freelancer phone",font=font).grid(row=3,column=0)
  free_phone = customtkinter.CTkEntry(left_tabs.tab("Add Freelancer"), placeholder_text="freelancer phone",width=240)
  free_phone.grid(row=3, column=1,padx=(5, 0), pady=(5, 5))

  customtkinter.CTkButton(left_tabs.tab("Add Freelancer"),command=AddFreelancer,text="Submit").grid(row=8,column=1)
  free_submit_status=customtkinter.CTkLabel(left_tabs.tab("Add Freelancer"),text="",font=font)
  free_submit_status.grid(row=4,column=1)

  # making the right tabs
  
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

  freelancer_frame=customtkinter.CTkFrame(right_tabs.tab("Freelancers"))# CAN BE making a tab scrollable
  freelancer_frame.place(relheight=1,relwidth=1)
  # top frame
  top_frame.configure(padx=2,pady=2)
  customtkinter.CTkLabel(top_frame,text="OutSourcery",font=font).grid(row=0,column=0,padx=20, pady=0)
  customtkinter.CTkButton(top_frame,text="Task completed",font=font,command=delete).grid(row=0,column=1,padx=20, pady=10)
  customtkinter.CTkButton(top_frame,text="Important note",font=font,command=important_note).grid(row=0,column=2,padx=20, pady=10)
  customtkinter.CTkButton(top_frame,text="Change password",font=font,command=change_pw).grid(row=0,column=3,padx=20, pady=10)
  customtkinter.CTkButton(top_frame,text="Assign Project",font=font,command=Assign_project).grid(row=0,column=4,padx=20, pady=10)
  
  #home
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

  # freelancer_frame
  treev_freelancer = tkinter.ttk.Treeview(freelancer_frame, selectmode ='browse')#extended helps to select multiple and none to none
  treev_freelancer.place(relheight=1, relwidth=1)
  
  treescrolly = tkinter.Scrollbar(freelancer_frame, orient="vertical", command=treev_freelancer.yview) # command means update the yaxis view of the widget
  treescrollx = tkinter.Scrollbar(freelancer_frame, orient="horizontal", command=treev_freelancer.xview) # command means update the xaxis view of the widget
  treev_freelancer.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set) # assign the scrollbars to the Treeview Widget
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
  staff_work(un)
