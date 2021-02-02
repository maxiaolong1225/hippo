import xlwt
from django.shortcuts import render,HttpResponse
from django.utils.encoding import escape_uri_path
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.permissions import IsAuthenticated
# Create your views here.
from . import models
from .serializers import HostModelSerializer,HostCategoryModelSerializer
from io import BytesIO, StringIO

from hippo_api.utils.handle_excel import read_host_excel_data
from hippo_api.utils.handle_key import AppSetting


class HostView(ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    queryset = models.Hosts.objects.filter(is_show=True, is_deleted=False)
    # queryset = models.Hosts.objects.all()
    serializer_class = HostModelSerializer


class HostCategoryView(ListAPIView):
    permission_classes = [IsAuthenticated, ]
    queryset = models.HostCategory.objects.filter(is_show=True, is_deleted=False)
    # queryset = models.HostCategory.objects.all()
    serializer_class = HostCategoryModelSerializer


class HostExcelView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        all_host_data = models.Hosts.objects.all().values('id','category','hostname','ip_addr','port','username','desc')

        ws = xlwt.Workbook(encoding='utf-8')
        st = ws.add_sheet("主机数据")

        st.write(0,0,'id')
        st.write(0,1,'category')
        st.write(0,2,'hostname')
        st.write(0,3,'ip_addr')
        st.write(0,4,'port')
        st.write(0,5,'username')
        st.write(0,6,'desc')
        excel_row = 1
        for  host_obj in all_host_data:
            st.write(excel_row,0,host_obj.get('id'))
            st.write(excel_row,1,host_obj.get('category'))
            st.write(excel_row,2,host_obj.get('hostname'))
            st.write(excel_row,3,host_obj.get('ip_addr'))
            st.write(excel_row,4,host_obj.get('port'))
            st.write(excel_row,5,host_obj.get('username'))
            st.write(excel_row,6,host_obj.get('desc'))
            excel_row +=1

        sio = BytesIO()
        ws.save(sio)
        sio.seek(0)
        response = HttpResponse(sio.getvalue(),content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename={}'.format(escape_uri_path('主机列表数据.xls'))
        response.write(sio.getvalue())  # 必须要给response写入一下数据，不然不生效

        return response

    def post(self,request):
        defalut_password = request.data.get('defalut_password')
        host_excel = request.data.get('host_excel')

        sio = BytesIO()
        for i in host_excel:
            sio.write(i)

        res_data = read_host_excel_data(sio, defalut_password)

        return Response(res_data)

class HostFileView(ViewSet):
    # 方法分发之前，先获取要操作的主机id和链接
    def dispatch(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        host_obj = models.Hosts.objects.get(pk=pk)
        pkey = AppSetting.get('private_key')
        cli = host_obj.get_ssh(pkey)
        self.cli = cli
        ret = super().dispatch(request, *args, **kwargs)

        return ret

    # get_folders获取某个目录的文件和文件夹信息列表
    def get_folders(self, request, pk):
        # cmd = request.query_params.get('cmd')  #

        cmd = request.query_params.get('cmd')  # ls  ls-a

        res_code, res_data = self.cli.exec_command(cmd)
        # print('!!!!!!!', res_code,res_data)
        return Response([res_code, res_data])
        # res_code, res_data = self.cli.exec_command(cmd)
        # print('!!!!!!!', res_code,res_data)
        # result = self.cli.list_dir_attr('/bin')

        # print()
        # file_info_list = []
        #
        # for i in result:
        #     file_info_dict = {
        #         'ks': i.ks,
        #         'st_uid': i.st_uid,
        #         'st_gid': i.st_gid,
        #         'st_mode': i.st_mode,
        #         'st_atime': i.st_atime,
        #         'st_mtime': i.st_mtime,
        #
        #     }
        #     file_info_list.append(file_info_dict)
        #
        # print('>>>>>>>>>',file_info_list)

    def download_file(self, request, pk, file_path):
        pass

    def upload_file(self, request, pk):
        folder_path = request.query_params.get('folder_path')  #/home

        file_obj = request.FILES.get('file')
        folder_path += f'/{file_obj.name}'  # /home/xx.txt
        # print(folder_path)
        file_size = file_obj.size

        try:
            self.cli.put_file_by_fl(file_obj, folder_path, self.file_upload_callback)
        except:
            return Response({'error': '文件上传失败,请联系管理员或者查看一下用户权限'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'msg': 'ok'})

    def delete_file(self, request, file_path):
        pass

    def file_upload_callback(self, n, k):
        print('>>>>>>>>>>>', n, k)


