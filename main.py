import flet as ft
from datetime import datetime, timedelta, date

class Job:
    def __init__(self, name, hourly_wage, transportation_costs):
        self.name = name
        self.hourly_wage = hourly_wage
        self.transportation_costs = transportation_costs

class Shift:
    def __init__(self, job, date, start_time, end_time, break_time):
        self.job = job
        self.date = date.date()  # datetimeオブジェクトをdateオブジェクトに変更。
        self.start_time = start_time
        self.end_time = end_time
        self.break_time = break_time

    def __str__(self):
        return f"{self.job.name} - {self.date.strftime('%Y-%m-%d')} - {self.start_time} to {self.end_time} - 休憩{self.break_time}"

class SalaryCalculator:
    @staticmethod
    def calculate_salary(shifts, year, month):
        total_salary = 0
        transportation_salary = 0
        for shift in shifts:
            if shift.date.year == year and shift.date.month == month:
                total_hours = ((shift.end_time - shift.start_time).seconds - shift.break_time.seconds) / 3600
                total_salary += total_hours * shift.job.hourly_wage
                transportation_salary += shift.job.transportation_costs
        return total_salary, transportation_salary

class Control:
    def __init__(self, user):
        self.user = user

    def add_job(self, name, hourly_wage, transportation_costs):
        self.user.jobs.append(Job(name, hourly_wage, transportation_costs))

    def add_shift(self, job_name, date, start_time, end_time, break_time):
        for job in self.user.jobs:
            if job.name == job_name:
                for shift in self.user.shifts:
                    if shift.date == date and (
                        (start_time < shift.end_time and start_time > shift.start_time) or
                        (end_time > shift.start_time and end_time < shift.end_time)
                    ):
                        return False
                self.user.shifts.append(Shift(job, date, start_time, end_time, break_time))
                return True
        return False

    def edit_shift(self, shift, start_time, end_time, break_time):
        shift.start_time = timedelta(hours=int(start_time.value.split('-')[0]), minutes=int(start_time.value.split('-')[1]))
        shift.end_time = timedelta(hours=int(end_time.value.split('-')[0]), minutes=int(end_time.value.split('-')[1]))
        shift.break_time = timedelta(hours=int(break_time.value.split('-')[0]), minutes=int(break_time.value.split('-')[1]))

    def delete_shift(self, shift):
        self.user.shifts.remove(shift)

    def get_shifts_by_month(self, year, month):
        return [shift for shift in self.user.shifts if shift.date.year == year and shift.date.month == month]

    def delete_job(control, job_name):
        control.user.jobs = [job for job in control.user.jobs if job.name != job_name]

class User:
    def __init__(self):
        self.jobs = [Job("mac", 1000, 500)]  # 初期値を設定
        self.shifts = [Shift(self.jobs[0], datetime(2000, 10, 10), timedelta(hours=10), timedelta(hours=17), timedelta(hours=1))]
        
## 以下画面に関すること
def main(page: ft.Page):
    user = User()
    control = Control(user)
    page.window_width = 600  # 幅
    page.window_height = 800  # 高さ

    def show_main_menu(e):  # メイン画面
        page.controls.clear()
        page.title = "メインメニュー"
        page.add(
            ft.Text("アルバイト"),
            ft.Row(
                [                   
                    ft.FloatingActionButton(icon=ft.icons.ADD,text="登録",expand=2, on_click=show_add_job),
                    ft.FloatingActionButton(icon=ft.icons.DELETE,text="削除",expand=2, on_click=show_delete_job),
                ]
            ),
            ft.Text("シフト"),
            ft.Row(
                [                 
                    ft.FloatingActionButton(icon=ft.icons.ADD,text="追加",expand=2, on_click=show_add_shift),
                    ft.FloatingActionButton(icon=ft.icons.EDIT_OUTLINED,expand=2,text="確認・編集", on_click=show_select_year_month),
                ]
            ),
            ft.Text("給与"),
            ft.Row(
                [
                    ft.FloatingActionButton(icon=ft.icons.CURRENCY_YEN,text="計算",expand=2, on_click=show_calculate_salary),
                ]
            )
        )
        page.update()

    def show_add_job(e):  # アルバイト登録画面
        page.title = "アルバイト登録"
        name = ft.TextField(label="名前")
        hourly_wage = ft.TextField(label="時給")
        transportation_costs = ft.TextField(label="交通費")

        def show_add_job_check(e):
            page.controls.clear()
            page.controls.append(
                ft.Column(
                    [
                        ft.Text(f"アルバイト名'{name.value}'"),
                        ft.Text(f"時給'{hourly_wage.value}'"),
                        ft.Text(f"交通費'{transportation_costs.value}'"),
                        ft.ElevatedButton("修正", on_click=show_add_job),
                        ft.ElevatedButton("確定", on_click=submit_add_job),

                    ]
                )
            )
            page.update()
        def submit_add_job(e):
            control.add_job(name.value, int(hourly_wage.value), int(transportation_costs.value))
            show_main_menu(e)  # メイン画面に戻る

        page.controls.clear()
        page.controls.append(
            ft.Column(
                [
                    name,
                    hourly_wage,
                    transportation_costs,
                    ft.ElevatedButton("登録", on_click=show_add_job_check),  # 上の関数(submit)を行う
                    ft.ElevatedButton("終了", on_click=show_main_menu),
                ]

            )
        )
        page.update()

    def show_add_shift(e):  # シフトの追加画面
        page.title = "アルバイト登録"
        if not user.jobs:
            page.controls.append(ft.Text("登録されているアルバイトがありません。", color=ft.colors.RED))
            page.update()
            return

        job_name = ft.Dropdown(label="名前", options=[ft.dropdown.Option(job.name) for job in user.jobs])
        date = ft.TextField(label="日付（YYYY-MM-DD）")
        start_time = ft.TextField(label="開始時刻（HH-MM）")
        end_time = ft.TextField(label="終了時刻（HH-MM）")
        break_time = ft.TextField(label="休憩時間（HH-MM）")

        def show_add_shif_check(e):
            page.controls.clear()
            page.controls.append(
                ft.Column(
                    [
                        ft.Text(f"アルバイト名'{job_name.value}'"),
                        ft.Text(f"日付'{date.value}'"),
                        ft.Text(f"開始時間'{start_time.value}'"),
                        ft.Text(f"終了時間'{end_time.value}'"),
                        ft.Text(f"休憩時間'{break_time.value}'"),
                        ft.ElevatedButton("修正", on_click=show_add_shift),
                        ft.ElevatedButton("確定", on_click=submit_add_shift)
                    ]
                )
            )
            page.update()
        def submit_add_shift(e):
            try:
                date_parsed = datetime.strptime(date.value, '%Y-%m-%d')
                date_parsed_r0 = date_parsed.date()#00:00:00を取り除く
            except:
                page.controls.append(ft.Text("入力に誤りがあります。", color=ft.colors.RED))
                page.update()
                return
            
            start_time_parsed = timedelta(hours=int(start_time.value.split('-')[0]), minutes=int(start_time.value.split('-')[1]))
            end_time_parsed = timedelta(hours=int(end_time.value.split('-')[0]), minutes=int(end_time.value.split('-')[1]))
            break_time_parsed = timedelta(hours=int(break_time.value.split('-')[0]), minutes=int(break_time.value.split('-')[1]))

            if start_time_parsed >= end_time_parsed:
                page.controls.append(ft.Text("開始時刻が終了時刻より後です。", color=ft.colors.RED))
                page.update()
                return
            


            # 同じ日のシフトを取り出して比較
            for shift in user.shifts:
                print(shift.date)
                print(date_parsed_r0)#シフト登録画面で入力された情報
                if shift.date == date_parsed_r0:
                    print("a")
                    if (start_time_parsed < shift.end_time and end_time_parsed > shift.start_time):
                        page.controls.append(ft.Text("重複するシフトがあります。", color=ft.colors.RED))
                        page.update()
                        return

            if control.add_shift(job_name.value, date_parsed, start_time_parsed, end_time_parsed, break_time_parsed):
                show_main_menu(e)
            else:
                page.controls.append(ft.Text("シフトの追加に失敗しました。", color=ft.colors.RED))
                page.update()

        page.controls.clear()
        page.controls.append(
            ft.Column(
                [
                    job_name,
                    date,
                    start_time,
                    end_time,
                    break_time,
                    ft.ElevatedButton("追加", on_click=show_add_shif_check),
                    ft.ElevatedButton("終了", on_click=show_main_menu),
                ]
            )
        )
        page.update()



    def show_select_year_month(e):  # 月選択画面
        page.title = "シフト確認・編集"
        year = ft.TextField(label="年（YYYY）")  # yearはテキストボックス
        month = ft.TextField(label="月（MM）")

        def submit_select_year_month(e):
            try:
                year_value = int(year.value)  # year.valueでyearに入力されている値の取得
                month_value = int(month.value)
                if 1 <= month_value <= 12:
                    show_calendar(year_value, month_value)
                else:
                    ft.alert("正しい月を入力してください。")
            except ValueError:
                ft.alert("正しい年と月を入力してください。")

        page.controls.clear()
        page.controls.append(
            ft.Column(
                [
                    year,
                    month,
                    ft.ElevatedButton("確認", on_click=submit_select_year_month),
                    ft.ElevatedButton("終了", on_click=show_main_menu),
                ]
            )
        )
        page.update()

    def show_calendar(year, month):
        shifts = control.get_shifts_by_month(year, month)
        calendar = ft.GridView(
            width=600,
            height=600,
            runs_count=7,
            spacing=5,
            run_spacing=5,
        )

        shift_details_container = ft.Column()  # シフト詳細を表示するためのコンテナ

        def show_shift_details(e):  # fletライブラリでイベントハンドラーに渡されるオブジェクト
            selected_date = e.control.data  # 下のcalender.controlsからdataだけを指定


            day_shifts = [shift for shift in shifts if shift.date == selected_date]
            shift_details = [ft.Text(str(shift)) for shift in day_shifts]

            shift_details_container.controls.clear()  # シフト詳細コンテナをクリア
            shift_details_container.controls.append(
                ft.Column(
                    [
                        ft.Text(f"{selected_date.strftime('%Y-%m-%d')} のシフト"),
                        *shift_details,
                    ]
                )
            )
            for shift in day_shifts:
                shift_details_container.controls.append(
                    ft.Row(
                        [
                            ft.ElevatedButton("編集", on_click=lambda e, shift=shift: show_edit_shift_screen(shift)),
                            ft.ElevatedButton("削除", on_click=lambda e, shift=shift: show_delete_shift_screen(shift))
                        ]
                    )
                )
            page.update()

        def show_edit_shift_screen(shift):
            shiftnew=shift
            start_time = ft.TextField(label="開始時間 (HH-MM)", value=f"{shift.start_time.seconds//3600:02d}-{(shift.start_time.seconds//60)%60:02d}")
            end_time = ft.TextField(label="終了時間 (HH-MM)", value=f"{shift.end_time.seconds//3600:02d}-{(shift.end_time.seconds//60)%60:02d}")
            break_time = ft.TextField(label="休憩時間 (HH-MM)", value=f"{shift.break_time.seconds//3600:02d}-{(shift.break_time.seconds//60)%60:02d}")

            def show_edit_shif_check(e,shiftnew):
                page.controls.clear()
                page.controls.append(
                    ft.Column(
                        [
                            ft.Text(f"開始時間'{start_time.value}'"),
                            ft.Text(f"終了時間'{end_time.value}'"),
                            ft.Text(f"休憩時間'{break_time.value}'"),
                            ft.ElevatedButton("修正", on_click=lambda e :show_edit_shift_screen(shiftnew)),                        
                            ft.ElevatedButton("確定", on_click=submit_edit_shift),
                        ]
                    )
                )
                page.update()

            def submit_edit_shift(e):
                start_time_parsed = timedelta(hours=int(start_time.value.split('-')[0]), minutes=int(start_time.value.split('-')[1]))
                end_time_parsed = timedelta(hours=int(end_time.value.split('-')[0]), minutes=int(end_time.value.split('-')[1]))
                break_time_parsed = timedelta(hours=int(break_time.value.split('-')[0]), minutes=int(break_time.value.split('-')[1]))

                if start_time_parsed >= end_time_parsed:
                    page.controls.append(ft.Text("開始時刻が終了時刻より後です。", color=ft.colors.RED))
                    page.update()
                    return
                
                # 同じ日のシフトを取り出して比較
                """
                for shift in user.shifts:

                    print("a")
                    print(start_time_parsed,end_time_parsed,shift.end_time,shift.start_time)

                
                    if shift.date == shift.date:
                        print("a")
                        if (start_time_parsed < shift.end_time and end_time_parsed > shift.start_time):
                            page.controls.append(ft.Text("重複するシフトがあります。", color=ft.colors.RED))
                            page.update()
                        return
                """

                
                control.edit_shift(shift, start_time, end_time, break_time)
                show_calendar(year, month)

            page.controls.clear()
            page.controls.append(
                ft.Column(
                    [
                        ft.Text("シフト編集"),
                        start_time,
                        end_time,
                        break_time,
                        ft.ElevatedButton("戻る", on_click=lambda e: show_calendar(year, month)),
                        ft.ElevatedButton("保存", on_click=lambda e :show_edit_shif_check(e,shiftnew)),
                    ]
                )
            )
            page.update()

        def show_delete_shift_screen(shift):
            def submit_delete_shift(e):
                control.delete_shift(shift)
                show_calendar(year, month)

            page.controls.clear()
            page.controls.append(
                ft.Column(
                    [
                        ft.Text(f"{shift.date}の{shift.start_time}-{shift.end_time}のシフトを削除しますか？"),
                        ft.ElevatedButton("戻る", on_click=lambda e: show_calendar(year, month)),
                        ft.ElevatedButton("削除", on_click=submit_delete_shift),
                    ]
                )
            )
            page.update()

        calendar.controls.clear()
        shift_details_container.controls.clear()  # シフト詳細コンテナをクリア

        # カレンダーのヘッダー
        #day_list=[ft.Text("日"),ft.Text("月"),ft.Text("火"),ft.Text("水"),ft.Text("木"),ft.Text("金"),ft.Text("土"),]
        #calendar.controls.__add__(ft.Row(day_list,spacing=75))
        
    
        calendar.controls.append(ft.Text("日"))
        calendar.controls.append(ft.Text("月"))
        calendar.controls.append(ft.Text("火"))
        calendar.controls.append(ft.Text("水"))
        calendar.controls.append(ft.Text("木"))
        calendar.controls.append(ft.Text("金"))
        calendar.controls.append(ft.Text("土"))
    
        

        # 月の初めの日の曜日を計算
        first_day = date(year, month, 1)
        start_weekday = first_day.weekday()

        # カレンダーに空の日付を追加
        for _ in range(start_weekday):
            calendar.controls.append(ft.Container())

        # カレンダーに日付を追加
        current_date = first_day
        while current_date.month == month:
            day_shifts = [shift for shift in shifts if shift.date == current_date]
            button_color = ft.colors.RED if day_shifts else ft.colors.GREY
            day_button = ft.ElevatedButton(
                text=str(current_date.day),
                data=current_date,
                on_click=show_shift_details,
                style=ft.ButtonStyle(color=button_color)
            )
            calendar.controls.append(day_button)
            current_date += timedelta(days=1)


        page.controls.clear()
        page.controls.append(
            ft.Column(
                [
                    ft.Text(f"{year}年{month}月"),
                    calendar,
                    shift_details_container,
                    ft.ElevatedButton("終了", on_click=show_main_menu)
                ]
            )
        )
        page.update()

    def show_calculate_salary(e):  # 給料計算画面
        page.title = "給料確認"
        year = ft.TextField(label="年（YYYY）")
        month = ft.TextField(label="月（MM）")

        def submit_calculate_salary(e):
            try:
                year_value = int(year.value)
                month_value = int(month.value)
                if 1 <= month_value <= 12:
                    today = datetime.now().date()

                    past_shifts = [shift for shift in user.shifts if shift.date <= today and shift.date.year == year_value and shift.date.month == month_value]
                    future_shifts = [shift for shift in user.shifts if shift.date > today and shift.date.year == year_value and shift.date.month == month_value]

                    past_salary, past_transportation = SalaryCalculator.calculate_salary(past_shifts, year_value, month_value)
                    total_salary, total_transportation = SalaryCalculator.calculate_salary(user.shifts, year_value, month_value)

                    page.controls.clear()
                    page.controls.append(
                        ft.Column(
                            [
                                ft.Text(f"{year_value}年{month_value}月の今日までの給料（交通費抜き）は: ¥{past_salary}"),
                                ft.Text(f"{year_value}年{month_value}月の今日までの給料（交通費込み）は: ¥{past_salary + past_transportation}"),
                                ft.Text(f"{year_value}年{month_value}月の今月の給料（交通費抜き）は: ¥{total_salary}"),
                                ft.Text(f"{year_value}年{month_value}月の今月の給料（交通費込み）は: ¥{total_salary + total_transportation}"),
                                ft.ElevatedButton("戻る", on_click=show_main_menu)
                            ]
                        )
                    )
                    page.update()
                else:
                        ft.alert("正しい月を入力してください。")
            except ValueError:
                    ft.alert("正しい年と月を入力してください。")

        page.controls.clear()
        page.controls.append(
            ft.Column(
                [
                    year,
                    month,
                    ft.ElevatedButton("計算", on_click=submit_calculate_salary),
                    ft.ElevatedButton("終了", on_click=show_main_menu),
                ]
            )
        )
        page.update()

    def show_delete_job(e):  # アルバイト削除画面
        page.title = "アルバイト削除"
        job_name = ft.Dropdown(label="削除するアルバイトの名前", options=[ft.dropdown.Option(job.name) for job in user.jobs])

        def get_job_by_name(name):
            for job in user.jobs:
                if job.name == name:
                    return job
            return None
        page.controls.clear()
        page.controls.append(
            ft.Row(
                [
                    job_name,
                    ft.ElevatedButton("削除", on_click=lambda e, :show_delete_job_check(e, get_job_by_name(job_name.value))),
                    ft.ElevatedButton("終了", on_click=show_main_menu),
                ]
            )
        )
        page.update()

    def show_delete_job_check(e,job_name):
        try:
            print(job_name.name)

        except AttributeError:
            print("a")

        def submit_delete_job(e):

            Control.delete_job(control, job_name.name)
            show_main_menu(e)  # メイン画面に戻る

        page.controls.clear()
        page.controls.append(
            ft.Column(
                [
                    ft.Text(f"アルバイト'{job_name.name}'を削除しますか？"),
                    ft.Text(f"アルバイト名: {job_name.name}"),
                    ft.Text(f"時給: {job_name.hourly_wage}"),
                    ft.Text(f"交通費: {job_name.transportation_costs}"),
                    ft.ElevatedButton("修正", on_click=show_delete_job),
                    ft.ElevatedButton("確定", on_click=submit_delete_job),
                ]
            )
        )
        page.update()

    show_main_menu(None)
    page.update()

ft.app(target=main)