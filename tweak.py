import customtkinter as ctk
import subprocess
import threading
import time
import arabic_reshaper
from bidi.algorithm import get_display

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class ArvanexUltimate(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("ARVANEX OS | Ultimate Control")
        self.geometry("1150x820")
        self.configure(fg_color="#0f0f0f")
        
        self.alpha = 0.0
        self.attributes("-alpha", self.alpha)
        
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = ctk.CTkFrame(self, width=260, corner_radius=0, fg_color="#161616")
        self.sidebar.grid(row=0, column=0, rowspan=2, sticky="nsew")
        
        self.logo = ctk.CTkLabel(self.sidebar, text="ARVANEX", font=ctk.CTkFont(family="Inter", size=28, weight="bold"), text_color="#ffffff")
        self.logo.grid(row=0, column=0, padx=20, pady=60)

        self.tabs = ctk.CTkTabview(
            self, 
            fg_color="#161616",
            segmented_button_fg_color="#222222",
            segmented_button_selected_color="#3b82f6",
            text_color="#ffffff",
            corner_radius=15
        )
        self.tabs.grid(row=0, column=1, padx=30, pady=(30, 10), sticky="nsew")

        self.t1 = self.tabs.add("Engine")
        self.t2 = self.tabs.add("Privacy")
        self.t3 = self.tabs.add("Gaming")
        self.t4 = self.tabs.add("Cleanup")

        self.selections = {}
        self.setup_modules()

        self.action_btn = ctk.CTkButton(
            self, 
            text="START OPTIMIZATION", 
            height=55, 
            corner_radius=12,
            fg_color="#3b82f6",
            hover_color="#1d4ed8",
            font=ctk.CTkFont(family="Inter", size=16, weight="bold"),
            command=self.ignite
        )
        self.action_btn.grid(row=1, column=1, padx=30, pady=30, sticky="ew")

        self.status = ctk.CTkLabel(self.sidebar, text="System: Ready", font=("Inter", 13), text_color="#666666")
        self.status.grid(row=1, column=0, pady=20)

        self.fade_in()

    def fix_text(self, text):
        reshaped_text = arabic_reshaper.reshape(text)
        return get_display(reshaped_text)

    def fade_in(self):
        if self.alpha < 1.0:
            self.alpha += 0.05
            self.attributes("-alpha", self.alpha)
            self.after(20, self.fade_in)

    def setup_modules(self):
        modules = {
            self.t1: {
                "GPU Acceleration": (f"({self.fix_text('تفعيل تسريع الجرافيك لتقليل التأخير')})", "reg add 'HKLM\\SYSTEM\\CurrentControlSet\\Control\\GraphicsDrivers' /v HwSchMode /t REG_DWORD /d 2 /f"),
                "Ultimate Power Plan": (f"({self.fix_text('تفعيل وضع الأداء الأقصى للطاقة')})", "powercfg -duplicatescheme e9a42b02-d5df-448d-aa00-03f14749eb61"),
                "Kernel Optimization": (f"({self.fix_text('تحسين استجابة نواة النظام للأوامر')})", "reg add 'HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile' /v SystemResponsiveness /t REG_DWORD /d 0 /f"),
                "Disable Power Saving": (f"({self.fix_text('تعطيل توفير الطاقة للمعالج')})", "powershell -Command \"Get-WmiObject -NS root\\cimv2 -Class Win32_Processor | % { $_.SetPowerState(1, 1) }\""),
                "RAM Compression": (f"({self.fix_text('تفعيل ضغط الرام لتوفير مساحة')})", "powershell -Command \"Enable-mmagent -mc\""),
                "Disable VBS Security": (f"({self.fix_text('تعطيل حماية VBS لزيادة الفريمات')})", "reg add 'HKLM\\SYSTEM\\CurrentControlSet\\Control\\DeviceGuard\\Scenarios\\HypervisorEnforcedCodeIntegrity' /v Enabled /t REG_DWORD /d 0 /f")
            },
            self.t2: {
                "Remove Telemetry": (f"({self.fix_text('حذف خدمات التجسس وجمع البيانات')})", "sc stop DiagTrack & sc config DiagTrack start=disabled & sc stop dmwappushservice & sc config dmwappushservice start=disabled"),
                "Disable Tracking": (f"({self.fix_text('منع تتبع النشاط داخل التطبيقات')})", "reg add 'HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\AppCompat' /v AITEnable /t REG_DWORD /d 0 /f"),
                "Kill Cortana/AI": (f"({self.fix_text('حذف كورتانا والمزامنة السحابية')})", "reg add 'HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\Windows Search' /v AllowCortana /t REG_DWORD /d 0 /f"),
                "Stop Activity History": (f"({self.fix_text('منع حفظ سجل النشاط الشخصي')})", "reg add 'HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\System' /v PublishUserActivities /t REG_DWORD /d 0 /f")
            },
            self.t3: {
                "Exclusive Fullscreen": (f"({self.fix_text('تحسين ملء الشاشة لتقليل التأخير')})", "reg add 'HKCU\\System\\GameConfigStore' /v GameDVR_FSEBehavior /t REG_DWORD /d 2 /f"),
                "No Mouse Acceleration": (f"({self.fix_text('تعطيل تسارع الماوس لدقة 1:1')})", "reg add 'HKCU\\Control Panel\\Mouse' /v MouseSpeed /t REG_SZ /d 0 /f"),
                "Low Latency Network": (f"({self.fix_text('تعديل حزم الشبكة لتقليل البنق')})", "reg add 'HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile' /v NetworkThrottlingIndex /t REG_DWORD /d 4294967295 /f"),
                "Fast Key Response": (f"({self.fix_text('تسريع استجابة الكيبورد')})", "reg add 'HKCU\\Control Panel\\Accessibility\\Keyboard Response' /v DelayBeforeAcceptance /t REG_SZ /d 0 /f")
            },
            self.t4: {
                "Wipe Bloatware": (f"({self.fix_text('حذف تطبيقات الويندوز غير الضرورية')})", "powershell -Command \"Get-AppxPackage | Remove-AppxPackage\""),
                "Deep Temp Cleanup": (f"({self.fix_text('تنظيف شامل لملفات النظام المؤقتة')})", "del /q/f/s %TEMP%\\* & del /q/f/s C:\\Windows\\Temp\\*"),
                "Shader Cache Reset": (f"({self.fix_text('تنظيف كاش كرت الشاشة')})", "del /q/f/s %LocalAppData%\\NVIDIA\\DXCache\\*"),
                "Flush DNS Cache": (f"({self.fix_text('تصفير سجلات DNS لتحسين الاتصال')})", "ipconfig /flushdns")
            }
        }

        for tab, data in modules.items():
            self.create_switches(tab, data)

    def create_switches(self, tab, data):
        frame = ctk.CTkScrollableFrame(tab, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        for name, (desc, cmd) in data.items():
            # دمج الاسم الإنجليزي مع العربي المصحح
            display_text = f"{name} {desc}"
            sw = ctk.CTkSwitch(
                frame, 
                text=display_text, 
                font=ctk.CTkFont(family="Inter", size=14), 
                progress_color="#3b82f6"
            )
            sw.pack(padx=20, pady=12, anchor="w")
            self.selections[name] = (sw, cmd)

    def ignite(self):
        def work():
            self.action_btn.configure(state="disabled", text="OPTIMIZING...")
            active = [(sw, cmd) for sw, cmd in self.selections.values() if sw.get()]
            
            for i, (sw, cmd) in enumerate(active, 1):
                self.status.configure(text=f"Task: {i}/{len(active)}", text_color="#3b82f6")
                subprocess.run(cmd, shell=True, capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
                time.sleep(0.12)

            self.status.configure(text="SUCCESS", text_color="#10b981")
            self.action_btn.configure(state="normal", text="START OPTIMIZATION")
            
        threading.Thread(target=work).start()

if __name__ == "__main__":
    app = ArvanexUltimate()
    app.mainloop()