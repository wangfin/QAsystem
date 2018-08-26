# 获取当前时间的前n天，前n周，前n月
import calendar
import datetime

class GetTime():
    # 获取前n天
    def get_days_before_today(self,n=0):
        '''''
        date format = "YYYY-MM-DD HH:MM:SS"
        '''
        now = datetime.datetime.now()
        if(n<0):
            return datetime.datetime(now.year, now.month, now.day, now.hour, now.minute, now.second)
        else:
            n_days_before = now - datetime.timedelta(days=n)
            return datetime.datetime(n_days_before.year, n_days_before.month, n_days_before.day, n_days_before.hour, n_days_before.minute, n_days_before.second)

    # 获取前n周
    def get_weeks_before_tody(self,n=0):
        '''''
        date format = "YYYY-MM-DD HH:MM:SS"
        '''
        now = datetime.datetime.now()
        if(n<0):
            return datetime.datetime(now.year, now.month, now.day, now.hour, now.minute, now.second)
        else:
            n_days_before = now - datetime.timedelta(days=n * 7)
            return datetime.datetime(n_days_before.year, n_days_before.month, n_days_before.day, n_days_before.hour, n_days_before.minute, n_days_before.second)

    # 获取前n月，准确的说是前30天
    def get_months_before_tody(self, n=0):
        '''''
        date format = "YYYY-MM-DD HH:MM:SS"
        '''
        now = datetime.datetime.now()
        if (n < 0):
            return datetime.datetime(now.year, now.month, now.day, now.hour, now.minute, now.second)
        else:
            n_days_before = now - datetime.timedelta(days=n * 30)
            return datetime.datetime(n_days_before.year, n_days_before.month, n_days_before.day, n_days_before.hour,
                                         n_days_before.minute, n_days_before.second)

    # 获取后n月 向前去需要输入负值
    def get_year_and_month(self,n=0):
        '''''
        get the year,month,days from today
        befor or after n months
        '''
        now = datetime.datetime.now()
        thisyear, thismon, thisday, thishour, thisminute, thissecond = self.get_now_time()
        totalmon = thismon + n

        if (n >= 0):
            if (totalmon <= 12):
                days = str(self.get_days_of_month(thisyear, totalmon))
                totalmon = self.add_zero(totalmon)
                return (thisyear, totalmon, days, thishour, thisminute, thissecond, thisday)
            else:
                i = totalmon / 12
                j = totalmon % 12
                if (j == 0):
                    i -= 1
                    j = 12
                thisyear += i
                days = str(self.get_days_of_month(thisyear, j))
                j = self.add_zero(j)
                return (str(thisyear), str(j), days, thishour, thisminute, thissecond, thisday)
        else:
            if ((totalmon > 0) and (totalmon < 12)):
                days = str(self.get_days_of_month(thisyear, totalmon))
                totalmon = self.add_zero(totalmon)
                return (thisyear, totalmon, days, thishour, thisminute, thissecond, thisday)
            else:
                i = totalmon / 12
                j = totalmon % 12
                if (j == 0):
                    i -= 1
                    j = 12
                thisyear += i
                days = str(self.get_days_of_month(thisyear, j))
                j = self.add_zero(j)
                return (str(thisyear), str(j), days, thishour, thisminute, thissecond, thisday)

    def get_now_time(self):
        now = datetime.datetime.now()
        thisyear = int(now.year)
        thismon = int(now.month)
        thisday = int(now.day)
        thishour = int(now.hour)
        thisminute = int(now.minute)
        thissecond = int(now.second)
        return thisyear, thismon, thisday, thishour, thisminute, thissecond

    def get_days_of_month(self,year, mon):
        return calendar.monthrange(year, mon)[1]

    def add_zero(self,n):
        '''''
        add 0 before 0-9
        return 01-09
        '''
        nabs = abs(int(n))
        if (nabs < 10):
            return "0" + str(nabs)
        else:
            return nabs

    def get_today_months(self,n=0):
        year, mon, d, hour, minute, second, day = self.get_year_and_month(n)
        arr = (year, mon, d, hour, minute, second, day)
        print(arr)
        if (int(day) < int(d)):
            arr = (year, mon, day, hour, minute, second)
        return "-".join("%s" % i for i in arr)

    def month_get(saelf,d=datetime.datetime.now()):
        dayscount = datetime.timedelta(days=d.day)
        dayto = d - dayscount
        date_from = datetime.datetime(dayto.year, dayto.month, 1, 0, 0, 0)
        date_to = datetime.datetime(dayto.year, dayto.month, dayto.day, 23, 59, 59)
        print('---'.join([str(date_from), str(date_to)]))

    # 从开始时间到结束时间的每一天
    # 可以调节timedelta来更改里面的间隔
    def dateRange(self,beginDate, endDate,n):
        dates = []
        dt = datetime.datetime.strptime(beginDate.split()[0], "%Y-%m-%d")
        # dt = datetime.datetime.strftime('%Y-%m-%d', dtime)
        # time_array = time.strptime(res.times, '%Y-%m-%d %H:%M:%S')
        # str_date = time.
        date = beginDate.split()[0]
        while date <= endDate.split()[0]:
            dates.append(date)
            dt = dt + datetime.timedelta(days=n)
            date = dt.strftime("%Y-%m-%d")
        return dates
    # 从开始时间到结束时间的小时
    # 可以更改timedelta(hours=1)来更改间隔
    def hourRange(self,beginDate, endDate,n):
        dates = []
        dt = datetime.datetime.strptime(beginDate, "%Y-%m-%d %H:%M:%S")
        # dt = datetime.datetime.strftime('%Y-%m-%d', dtime)
        # time_array = time.strptime(res.times, '%Y-%m-%d %H:%M:%S')
        # str_date = time.
        date = beginDate
        while date <= endDate:
            dates.append(date)
            dt = dt + datetime.timedelta(hours=n)
            date = dt.strftime("%Y-%m-%d %H:%M:%S")
        return dates

if __name__ == '__main__':
    gettime = GetTime()
    print(gettime.get_weeks_before_tody(1))
    print(gettime.get_days_before_today(1))
    print(gettime.get_months_before_tody(1))
    print(gettime.month_get())
    print(gettime.dateRange('2018-07-25 11:10:03','2018-08-24 11:10:03',n=5))
    # print(gettime.hourRange('2018-08-01 17:23:21', '2018-08-02 17:23:21'))

