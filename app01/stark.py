from .models import *
from django.conf.urls import url
from django.http import JsonResponse
from django.utils.safestring import mark_safe
from stark.service.sites import site, ModelStark
from django.shortcuts import HttpResponse, redirect, render

site.register(Oreder)
site.register(Department)
site.register(UserInfo)
site.register(School)
site.register(Course)


# 自定义的classlist显示
class ClassConfig(ModelStark):
    list_display = ["course", "semester", "price", "teachers", "tutor"]


site.register(ClassList, ClassConfig)


# 自定义的customer显示
class CustomerConfig(ModelStark):

    def display_gender(self, obj=None, is_header=False):
        if is_header:
            return "性别"
        # 找到对应的字符串
        return obj.get_gender_display()

    def display_course(self, obj=None, is_header=False):
        if is_header:
            return "咨询课程"
        link_list = []
        for course in obj.course.all():
            s = "<a>%s</a>" % (course.name)
            link_list.append(s)
        return mark_safe("".join(link_list))

    list_display = ["name", display_gender, "graduation_school", "course", display_course]


site.register(Customer, CustomerConfig)
site.register(ConsultRecord)


# 自定义的StudentConfig显示
class StudentConfig(ModelStark):
    # 自定义列显示详细信息
    def display_score(self, obj=None,is_header=False):
        if is_header:
            return "详细信息"
        return mark_safe("<a href='/stark/app01/student/%s/info/'>详细信息</a>"%obj.pk)

    # 视图函数
    def student_info(self, request, sid):
        if request.is_ajax():
            cid = request.GET.get("cid")
            # 查询学生sid在班级cid下的所有的学生学习记录对象
            studentstudyrecord_list = StudentStudyRecord.objects.filter(student=sid,classstudyrecord__class_obj=cid)
            ret = [["day%s" % studentstudyrecord.classstudyrecord.day_num,studentstudyrecord.score ] for studentstudyrecord in studentstudyrecord_list]
            return JsonResponse(ret,safe=False)
        # 获取学生对象
        student_obj = Student.objects.filter(pk=sid).first()
        # 获取对应的班级
        class_list = student_obj.class_list.all()
        return render(request, "student_info.html", locals())

    # 额外路由
    def extra_url(self):
        temp=[]
        temp.append(url("(\d+)/info/",self.student_info))
        return temp

    list_display = ["customer", "class_list", display_score]


site.register(Student, StudentConfig)


# 自定义ClassStudyRecord显示
class ClassStudyRecordConfig(ModelStark):
    def record_score(self, request, cls_record_id):
        # 方式1：用ajax修改
        if request.is_ajax():
            action = request.POST.get("action")
            sid = request.POST.get("sid")
            val = request.POST.get("val")
            # 修改成绩
            StudentStudyRecord.objects.filter(pk=sid).update(**{action:val})
            return HttpResponse("ok")
        # 方式2：用button按钮保存
        if request.method == "POST":
            # print(request.POST)
            '''
            {'score_1': ['85'], 'homework_note_4': ['22221'], 'homework_note_1': ['很好!1'], 'score_4': ['40'],
             'csrfmiddlewaretoken': ['dEtTvvxQvuhQh5wtGGI8wNAIh5oBD8roBnl6WfZXbykoQwcSQHxyPFKe78MWhNzZ']}
            '''
            #   但是我们想要这种效果
            '''
                   {
                     1:{score:50,homework_note:12323},
                     2:{score:80,homework_note:456},
                    }
                   
            '''
            dic = {}
            for key, val in request.POST.items():
                # 因为这个里边包含id值和字段
                if key == "csrfmiddlewaretoken":
                    continue
                field, pk = key.rsplit("_", 1)
                if pk in dic:
                    dic[pk][field] = val
                else:
                    dic[pk] = {field: val}
            for pk, update_data in dic.items():
                # 更新数据
                StudentStudyRecord.objects.filter(pk=pk).update(**update_data)

            # 当前页面
            return redirect(request.path)

        # 班级学习记录对象
        cls_record = ClassStudyRecord.objects.get(pk=cls_record_id)
        # 该班级学习记录对象关联的所有的学生学习记录对象,反向查询
        studentstudyrecord_list = cls_record.studentstudyrecord_set.all()
        # 获取成绩
        score_choice =StudentStudyRecord.score_choices
        return render(request, "record_score.html", locals())

    # 保存成绩的额外路由
    def extra_url(self):
        temp = []
        temp.append(url("(\d+)/record_score/",self.record_score))
        return temp

    # 自定义一列显示录入成绩，要有新的路径，所以要用额外路由
    def handle_score(self, obj=None, is_header=False):
        if is_header:
            return "录入成绩"
        return mark_safe("<a href='/stark/app01/classstudyrecord/%s/record_score/'>录入成绩</a>" % (obj.pk))

    # 自定义一列显示详细信息
    def display_info(self, obj=None, is_header=False):
        if is_header:
            return "详细信息"
        return mark_safe("<a href='/stark/app01/studentstudyrecord/?classstudyrecord=%s'>详细信息</a>" % obj.pk)

    list_display = ["class_obj", "day_num", "teacher", "course_title", display_info, handle_score]

    # action批量处理，批量创建关联的学生学习记录
    def patch_init(self, request, queryset):
        for cls_study_obj in queryset:
            # 查询班级关联的所有的学生
            # 先查找到班级ClassStudyRecord与Classlist正向关联
            # 然后班级和Student表反向关联，反向查询
            student_list = cls_study_obj.class_obj.student_set.all()
            ssr_list = []
            for student in student_list:
                # 创建数据
                ssr = StudentStudyRecord(student=student, classstudyrecord=cls_study_obj)
                ssr_list.append(ssr)
            # 这样创建是为了减少数据库的压力
            StudentStudyRecord.objects.bulk_create(ssr_list)

    patch_init.desc = "创建关联学生学习记录"
    actions = [patch_init]


site.register(ClassStudyRecord, ClassStudyRecordConfig)


# 自定义StudentStudyRecord显示
class StudentStudyRecordConfig(ModelStark):
    # 自定义显示出勤
    def display_record(self, obj=None, is_header=False):
        if is_header:
            return "出勤"
        html = "<select name='record' class='record' pk=%s>" % obj.pk
        for item in StudentStudyRecord.record_choices:
            # ('checked', '已签到')
            # ('vacate', '请假')
            # ('late', '迟到')
            # ('noshow', '缺勤')
            # ('leave_early', '早退')
            if obj.record == item[0]:
                option = "<option selected value='%s'>%s</option>" % (item[0], item[1])
            else:
                option = "<option value='%s'>%s</option>" % (item[0], item[1])
            html += option
        html += "</select>"
        return mark_safe(html)

    # 显示成绩自定义列
    def display_score(self, obj=None, is_header=False):
        if is_header:
            return "成绩"
        return obj.get_score_display()

    list_display = ["student", "classstudyrecord", display_score, display_record]

    # 第一种方式：批量处理出勤
    def patch_late(self, request, queryset):
        queryset.update(record="late")

    patch_late.desc = "迟到"
    actions = [patch_late]

    # 第二种处理方式：ajax
    def edit_record(self, request, id):
        record = request.POST.get("record")
        StudentStudyRecord.objects.filter(pk=id).update(record=record)
        return HttpResponse("ok")

    def extra_url(self):
        temp = []
        temp.append(url(r"(\d+)/edit_record/$", self.edit_record))
        return temp


site.register(StudentStudyRecord, StudentStudyRecordConfig)
