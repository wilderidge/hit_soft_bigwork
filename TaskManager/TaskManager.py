import streamlit as st
import re
import json

from TaskManager.qw import qw_chat

prompt = """现在你需要完成一个总结任务，你需要总结一段旅游助手和用户之间的对话并归纳成任务和详细流程，具体来说。你需要返回一个json字典
        {“任务名字1”:“任务详细情况”，“任务名字2”:“任务详细情况”……}，任务名字应该从下面几个中选择
        交通方式建议和规划,美食和景点推荐,景点实时语音讲解,规划住宿
        任务详细情况应该包括该任务最终的详细信息
        不要输出除了json字典以外的其他内容"""





class Task_Manager():
    def __init__(self):
        self.tasks = []

    def show_task_list(self):
        for i in range(len(self.tasks)):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f'#### 任务:{i}：{self.tasks[i]["task_name"]}')
            with col2:
                @st.experimental_dialog("查看任务详情",width="large")
                def show_task():
                    st.markdown("##### "+self.tasks[i]["task_name"])
                    st.write(self.tasks[i]["task_detail"])
                if st.button(f"查看任务{i}详情"):
                    show_task()

            # st.markdown(f'#### Task:{i}：{i}')
            # st.write(f'#### Task:{i}：6666')
            # #if st.button(f"查看任务{i}详情"):
            # show_task()
            # st.divider()
        # for task in self.tasks:
        #     st.markdown(f'#### Task:{task.id}')
        #     st.divider('rainbow')

    # def show_task_detail(self, task_id):
    #     task = self.get_task_by_id(task_id)
    #     if task:
    #         st.write(f"任务ID:{task['task_id']}, 任务名称:{task['task_name']}, "
    #                  f"任务状态:{task['task_status']}, 任务优先级:{task['task_priority']}")
    #     else:
    #         st.write("任务不存在")
    def refresh(self):
        context = prompt
        question = '\n'
        for msg in st.session_state.messages:
            if msg["content"] != prompt:
                question += msg["role"] + ":" + msg["content"] + '\n'
        dialogue = qw_chat(context, question)
        pattern = r"{(.*?)}"

        # 搜索匹配的JSON字符串
        match = re.search(pattern, dialogue, re.DOTALL)
        self.tasks = []
        if match:
            json_str = match.group(1)

            try:
                print(json_str)
                data = json.loads("{" + json_str + "}")
                for key, value in data.items():
                    self.add_task(key, value)
            except json.JSONDecodeError as e:
                print("Error decoding JSON:", e)

        else:
            print("No JSON data found in the text.")

    def add_task(self, task_name, task_detail):
        task_id = len(self.tasks) + 1
        task = {
            "task_id": task_id,
            "task_name": task_name,
            "task_detail": task_detail,
        }
        self.tasks.append(task)
