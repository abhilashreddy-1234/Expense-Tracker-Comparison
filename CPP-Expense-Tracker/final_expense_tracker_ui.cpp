#include <windows.h>
#include <vector>
#include <string>
#include <sstream>
#include <fstream>
#include <iomanip>

using namespace std;

struct Expense {
    string date;
    double amount;
    string category;
    string description;
};

vector<Expense> expenses;

HWND hDate, hAmount, hCategory, hDescription;
HWND hList, hTotalLabel;
HWND hFilterCategory, hStartDate, hEndDate;

COLORREF bgColor = RGB(25,25,35);
HBRUSH bgBrush;

// Convert MM-DD-YYYY safely
int ConvertDateToInt(const string& date) {
    if(date.length() != 10) return -1;

    if(date[2] != '-' || date[5] != '-') return -1;

    try {
        string yyyy = date.substr(6,4);
        string mm = date.substr(0,2);
        string dd = date.substr(3,2);
        return stoi(yyyy + mm + dd);
    }
    catch(...) {
        return -1;
    }
}

void UpdateExpenseList(const vector<Expense>& listToShow) {

    SendMessage(hList, LB_RESETCONTENT, 0, 0);

    double total = 0;

    for(const auto &e : listToShow) {

        stringstream ss;
        ss << e.date << " | $"
           << fixed << setprecision(2) << e.amount
           << " | " << e.category
           << " | " << e.description;

        SendMessage(hList, LB_ADDSTRING, 0, (LPARAM)ss.str().c_str());

        total += e.amount;
    }

    stringstream totalText;
    totalText << "Total: $" << fixed << setprecision(2) << total;
    SetWindowText(hTotalLabel, totalText.str().c_str());
}

void SaveToFile() {

    ofstream file("expenses.csv");
    file << "Date,Amount,Category,Description\n";

    for(const auto &e : expenses) {
        file << e.date << ","
             << fixed << setprecision(2) << e.amount << ","
             << e.category << ","
             << e.description << "\n";
    }

    file.close();
}

void LoadFromFile() {

    expenses.clear();

    ifstream file("expenses.csv");
    if(!file.is_open()) return;

    string line;
    getline(file,line); // skip header

    while(getline(file,line)) {

        stringstream ss(line);
        string d,a,c,desc;

        getline(ss,d,',');
        getline(ss,a,',');
        getline(ss,c,',');
        getline(ss,desc);

        try {
            expenses.push_back({d, stod(a), c, desc});
        } catch(...) {}
    }

    file.close();
    UpdateExpenseList(expenses);
}

void DeleteSelected() {

    int index = SendMessage(hList, LB_GETCURSEL, 0, 0);

    if(index == LB_ERR) return;

    expenses.erase(expenses.begin() + index);

    SaveToFile();   // 🔥 now delete updates CSV also
    UpdateExpenseList(expenses);
}

LRESULT CALLBACK WindowProc(HWND hwnd, UINT msg, WPARAM wParam, LPARAM lParam) {

    switch(msg) {

    case WM_CREATE:
    {
        bgBrush = CreateSolidBrush(bgColor);

        CreateWindow("STATIC","Date (MM-DD-YYYY):",
            WS_VISIBLE|WS_CHILD,
            40,40,200,20,
            hwnd,NULL,NULL,NULL);

        hDate = CreateWindow("EDIT","",
            WS_VISIBLE|WS_CHILD|WS_BORDER,
            220,40,200,25,
            hwnd,NULL,NULL,NULL);

        CreateWindow("STATIC","Amount:",
            WS_VISIBLE|WS_CHILD,
            40,80,200,20,
            hwnd,NULL,NULL,NULL);

        hAmount = CreateWindow("EDIT","",
            WS_VISIBLE|WS_CHILD|WS_BORDER,
            220,80,200,25,
            hwnd,NULL,NULL,NULL);

        CreateWindow("STATIC","Category:",
            WS_VISIBLE|WS_CHILD,
            40,120,200,20,
            hwnd,NULL,NULL,NULL);

        hCategory = CreateWindow("EDIT","",
            WS_VISIBLE|WS_CHILD|WS_BORDER,
            220,120,200,25,
            hwnd,NULL,NULL,NULL);

        CreateWindow("STATIC","Description:",
            WS_VISIBLE|WS_CHILD,
            40,160,200,20,
            hwnd,NULL,NULL,NULL);

        hDescription = CreateWindow("EDIT","",
            WS_VISIBLE|WS_CHILD|WS_BORDER,
            220,160,200,25,
            hwnd,NULL,NULL,NULL);

        CreateWindow("BUTTON","Add",
            WS_VISIBLE|WS_CHILD,
            480,40,120,30,
            hwnd,(HMENU)1,NULL,NULL);

        CreateWindow("BUTTON","Delete",
            WS_VISIBLE|WS_CHILD,
            480,80,120,30,
            hwnd,(HMENU)2,NULL,NULL);

        CreateWindow("BUTTON","Save",
            WS_VISIBLE|WS_CHILD,
            480,120,120,30,
            hwnd,(HMENU)3,NULL,NULL);

        CreateWindow("BUTTON","Load",
            WS_VISIBLE|WS_CHILD,
            480,160,120,30,
            hwnd,(HMENU)4,NULL,NULL);

        hList = CreateWindow("LISTBOX","",
            WS_VISIBLE|WS_CHILD|WS_BORDER|LBS_STANDARD,
            40,220,900,300,
            hwnd,NULL,NULL,NULL);

        CreateWindow("STATIC","Filter Category:",
            WS_VISIBLE|WS_CHILD,
            40,550,200,20,
            hwnd,NULL,NULL,NULL);

        hFilterCategory = CreateWindow("EDIT","",
            WS_VISIBLE|WS_CHILD|WS_BORDER,
            220,550,200,25,
            hwnd,NULL,NULL,NULL);

        CreateWindow("BUTTON","Apply Filter",
            WS_VISIBLE|WS_CHILD,
            450,550,150,30,
            hwnd,(HMENU)5,NULL,NULL);

        CreateWindow("STATIC","Start Date:",
            WS_VISIBLE|WS_CHILD,
            40,590,200,20,
            hwnd,NULL,NULL,NULL);

        hStartDate = CreateWindow("EDIT","",
            WS_VISIBLE|WS_CHILD|WS_BORDER,
            220,590,200,25,
            hwnd,NULL,NULL,NULL);

        CreateWindow("STATIC","End Date:",
            WS_VISIBLE|WS_CHILD,
            450,590,200,20,
            hwnd,NULL,NULL,NULL);

        hEndDate = CreateWindow("EDIT","",
            WS_VISIBLE|WS_CHILD|WS_BORDER,
            620,590,200,25,
            hwnd,NULL,NULL,NULL);

        CreateWindow("BUTTON","Date Filter",
            WS_VISIBLE|WS_CHILD,
            220,630,150,30,
            hwnd,(HMENU)6,NULL,NULL);

        CreateWindow("BUTTON","Show All",
            WS_VISIBLE|WS_CHILD,
            400,630,150,30,
            hwnd,(HMENU)7,NULL,NULL);

        hTotalLabel = CreateWindow("STATIC","Total: $0.00",
            WS_VISIBLE|WS_CHILD,
            40,680,400,30,
            hwnd,NULL,NULL,NULL);

        break;
    }

    case WM_COMMAND:
    {
        if(LOWORD(wParam)==1) {
            char d[100],a[100],c[100],desc[200];

            GetWindowText(hDate,d,100);
            GetWindowText(hAmount,a,100);
            GetWindowText(hCategory,c,100);
            GetWindowText(hDescription,desc,200);

            try {
                expenses.push_back({d,stod(a),c,desc});
                SaveToFile();
                UpdateExpenseList(expenses);
            } catch(...) {
                MessageBox(hwnd,"Invalid amount","Error",MB_OK);
            }
        }

        if(LOWORD(wParam)==2) DeleteSelected();
        if(LOWORD(wParam)==3) SaveToFile();
        if(LOWORD(wParam)==4) LoadFromFile();

        if(LOWORD(wParam)==5) {
            char filter[100];
            GetWindowText(hFilterCategory,filter,100);

            vector<Expense> filtered;

            for(auto &e:expenses)
                if(e.category == filter)
                    filtered.push_back(e);

            UpdateExpenseList(filtered);
        }

        if(LOWORD(wParam)==6) {

            char s[100],e[100];
            GetWindowText(hStartDate,s,100);
            GetWindowText(hEndDate,e,100);

            int startInt = ConvertDateToInt(s);
            int endInt   = ConvertDateToInt(e);

            if(startInt == -1 || endInt == -1) {
                MessageBox(hwnd,"Invalid date format.\nUse MM-DD-YYYY","Error",MB_OK);
                break;
            }

            if(endInt < startInt) {
                MessageBox(hwnd,"End date must be after start date","Error",MB_OK);
                break;
            }

            vector<Expense> filtered;

            for(auto &x:expenses) {
                int d = ConvertDateToInt(x.date);
                if(d >= startInt && d <= endInt)
                    filtered.push_back(x);
            }

            UpdateExpenseList(filtered);
        }

        if(LOWORD(wParam)==7) UpdateExpenseList(expenses);

        break;
    }

    case WM_CTLCOLORSTATIC:
    case WM_CTLCOLOREDIT:
    case WM_CTLCOLORLISTBOX:
        SetTextColor((HDC)wParam,RGB(255,255,255));
        SetBkColor((HDC)wParam,bgColor);
        return (LRESULT)bgBrush;

    case WM_DESTROY:
        PostQuitMessage(0);
        return 0;
    }

    return DefWindowProc(hwnd,msg,wParam,lParam);
}

int WINAPI WinMain(HINSTANCE hInstance,HINSTANCE,LPSTR,int){

    const char CLASS_NAME[]="ExpenseTracker";

    WNDCLASS wc={};
    wc.lpfnWndProc=WindowProc;
    wc.hInstance=hInstance;
    wc.lpszClassName=CLASS_NAME;
    wc.hbrBackground=CreateSolidBrush(bgColor);

    RegisterClass(&wc);

    HWND hwnd=CreateWindowEx(
        0,CLASS_NAME,
        "Expense Tracker - STABLE FINAL VERSION",
        WS_OVERLAPPEDWINDOW,
        CW_USEDEFAULT,CW_USEDEFAULT,
        1000,800,
        NULL,NULL,hInstance,NULL);

    ShowWindow(hwnd, SW_MAXIMIZE);

    MSG msg={};
    while(GetMessage(&msg,NULL,0,0)){
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }

    return 0;
}