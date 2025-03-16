from simple_blogger import CommonBlogger
from simple_blogger.generators.OpenAIGenerator import OpenAITextGenerator
from datetime import datetime
from simple_blogger.senders.TelegramSender import TelegramSender
from simple_blogger.senders.InstagramSender import InstagramSender

class Project(CommonBlogger):
    def _example_task_creator(self):
        return [
            {
                "skill": "Skill",
                "group": "Group"
            }
        ]

    def _get_category_folder(self, task):
        return f"{task['group']}"
                    
    def _get_topic_folder(self, task):
        return f"{task['skill']}"

    def _system_prompt(self, task):
        return "Ты - блогер с 1000000 миллионном подписчиков"

    def _task_converter(self, idea):
        return { 
                    "group": idea['group'],
                    "skill": idea['skill'],
                    "topic_prompt": f"Расскажи как {idea['skill']}, используй не более {self.topic_word_limit} слов, используй смайлики",
                    "topic_image": f"Нарисуй рисунок, вдохновлённый темой '{idea['skill']}'",
                }

    def __init__(self, **kwargs):
        super().__init__(
            first_post_date=datetime(2025, 2, 19),
            text_generator=OpenAITextGenerator(),
            topic_word_limit=100,
            reviewer=TelegramSender(),
            senders=[TelegramSender(channel_id=f"@one_day_skill"), InstagramSender(channel_token_name="ONE_DAY_SKILL_TOKEN")],
            **kwargs
        )

    