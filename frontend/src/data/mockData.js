export const documents = [
  {id:1,name:"Employee_Handbook_2023.pdf",type:"PDF",date:"Oct 12, 2023",status:"Ready"},
  {id:2,name:"Q3_Financial_Report_Final.docx",type:"DOCX",date:"Oct 24, 2023",status:"Processing"},
  {id:3,name:"Client_Contact_List_Updated.csv",type:"CSV",date:"Oct 22, 2023",status:"Ready"}
];

export const messages = [
  {id:1,role:"user",text:"What is the attendance requirement?"},
  {id:2,role:"ai",text:"According to the uploaded knowledge base, students must maintain 75% attendance across their registered courses.",source:{name:"Employee_Handbook_2023.pdf",page:12,excerpt:"Students must maintain 75% attendance across their registered courses."}}
];