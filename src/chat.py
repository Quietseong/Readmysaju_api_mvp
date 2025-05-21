# src/chat.py
from typing import Dict, List, Optional
from dataclasses import dataclass
import json, time
import openai
from dotenv import load_dotenv
import os
from IPython.display import HTML, display

# .env 파일에서 API 키 로드
load_dotenv()

@dataclass
class Tone:
    name: str
    description: str
    characteristics: List[str]
    example: str

class Chat:
    def __init__(self, system_content_path: str = "data/system_prompt.json"):
        """
        Chat 클래스의 초기화 함수입니다.
        
        Args:
            system_content_path (str): 시스템 프롬프트가 저장된 JSON 파일의 경로입니다.
                기본값은 'data/system_prompt.json'입니다.
        """
        # JSON 파일에서 시스템 프롬프트를 읽어옵니다
        with open(system_content_path, 'r', encoding='utf-8') as f:
            system_prompt_data = json.load(f)
            
            # 기본 역할 설정
            self.role = system_prompt_data['role']
            
            # 톤 관리 설정
            self.tones: Dict[str, Tone] = {}
            for tone_key, tone_data in system_prompt_data['interpretation_tones'].items():
                self.tones[tone_key] = Tone(
                    name=tone_data['name'],
                    description=tone_data['description'],
                    characteristics=tone_data['characteristics'],
                    example=tone_data['example']
                )
            
            # 대화 흐름 설정
            self.conversation_flow = system_prompt_data['conversation_flow']
            
            # 범위 외 응답 설정
            self.out_of_scope_response = system_prompt_data['out_of_scope_response']
            
            # 현재 선택된 톤 (기본값: cute_fortune_teller)
            self.current_tone: str = "cute_fortune_teller"
            
            # 대화 기록 초기화
            self.messages: List[Dict] = []
            
            # 시스템 메시지 초기화
            self.init_messages()

    def init_messages(self) -> None:
        """시스템 메시지를 초기화합니다."""
        self.messages = []
        
        # 기본 역할 메시지
        self.add_system_content(f"You are {self.role}.")
        
        # 현재 톤에 대한 메시지
        current_tone = self.tones[self.current_tone]
        tone_message = f"""You are speaking in the {current_tone.name} tone.
                        Characteristics:
                        {chr(10).join(f'- {char}' for char in current_tone.characteristics)}
                        Example: {current_tone.example}"""
        self.add_system_content(tone_message)
        
        # 대화 흐름에 대한 메시지
        flow_message = f"""Follow this conversation flow:
                        1. First, ask for the user's:
                        {chr(10).join(f'- {q}' for q in self.conversation_flow['initial_questions'])}
        
                        2. When interpreting specific aspects, structure your response as:
                        {self.conversation_flow['response_structure']}
                        
                        3. Always end your responses with:
                        {self.conversation_flow['closing_question']}"""
        self.add_system_content(flow_message)

    def add_user_content(self, content: str) -> None:
        """사용자 메시지를 추가합니다."""
        self.messages.append({"role": "user", "content": content})
        
    def add_assistant_content(self, content: str) -> None:
        """어시스턴트 메시지를 추가합니다."""
        self.messages.append({"role": "assistant", "content": content})
        
    def add_system_content(self, content: str) -> None:
        """시스템 메시지를 추가합니다."""
        self.messages.append({"role": "system", "content": content})

    def change_tone(self, tone_key: str) -> None:
        """
        대화 톤을 변경합니다.
        Args:
            tone_key (str): 변경할 톤의 키값
        """
        if tone_key not in self.tones:
            raise ValueError(f"Invalid tone key: {tone_key}")
        self.current_tone = tone_key
        self.init_messages()  # 시스템 메시지 재초기화

    def _run_query(self):
        """에러 발생 시 재시도하는 코드"""
        max_retries = 7
        wait_time = 1

        for i in range(max_retries):
            try:
                self.response = openai.chat.completions.create(
                    model="gpt-4.1-nano-2025-04-14",
                    messages=self.messages,
                    temperature=0.7,
                    top_p=0.8
                )
                return
            except Exception as e:
                if i == max_retries - 1:
                    raise e
                else:
                    print(f"Excepption {e}. Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                    wait_time *= 2

    def query(self, content: str, print_response: bool = True) -> str:
        """
        GPT에 쿼리를 보내고 응답을 받습니다.
        
        Args:
            content (str): 사용자 메시지
            print_response (bool): 응답을 출력할지 여부
            
        Returns:
            str: GPT의 응답
        """
        self._run_query()
        # 범위를 벗어난 질문인지 확인하는 시스템 메시지 추가
        scope_check_message = {
            "role": "system",
            "content": f"""If the user's question is not related to Saju or fortune telling, 
            respond with: {self.out_of_scope_response}
            Only proceed with the normal response if the question is about Saju or fortune telling."""
        }
        
        # 임시 메시지 목록 생성 (원본 메시지 + 범위 체크 메시지)
        temp_messages = self.messages + [scope_check_message]
        
        # 사용자 메시지 추가
        temp_messages.append({"role": "user", "content": content})
        
        # GPT에 쿼리
        self.response = openai.chat.completions.create(
            model="gpt-4.1-nano-2025-04-14",
            messages=temp_messages,
            temperature=0.7,
            top_p=0.8
        )
        
        response_content = self.response.choices[0].message.content
        
        # 응답이 범위를 벗어난 경우의 메시지인지 확인
        if response_content.strip() == self.out_of_scope_response.strip():
            # 범위를 벗어난 경우, 대화 기록에 추가하지 않고 바로 반환
            if print_response:
                print(response_content)
            return response_content
        
        # 정상적인 사주 관련 질문인 경우, 대화 기록에 추가
        self.add_user_content(content)
        self.add_assistant_content(response_content)
        
        if print_response:
            print(response_content)
        return response_content

    def print_messages(self):
        for d in self.messages:
            role = d['role']
            content = d['content']
            if role == 'assistant':
                display(HTML(content))
            else:
                color = '#080' if role == 'system' else '#008'
                display(HTML(f"<span style='color: {color}'><b>{role}</b>: {content}</span>"))
