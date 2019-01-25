import pytest
import json
import os
from io import StringIO 
from dotenv import load_dotenv
import sys
sys.path.append('/home/mfriszky/worksworksworks/RESTKnot/CLI')

from libs import auth
FOLDER = os.path.expanduser("~")
class TestLogin:
    @pytest.mark.run(order=0)
    def test_login_success(self,monkeypatch):
        auth.load_env_file()
        user = os.environ.get('OS_USERNAME')
        pwd  = os.environ.get('OS_PASSWORD')

        monkeypatch.setattr('builtins.input', lambda x : user)
        monkeypatch.setattr('getpass.getpass', lambda x : pwd)

        output = auth.signin()
        assert output == True

    @pytest.mark.run(order=1)
    def test_logout_soft(self):
        for i in range(2):
            auth.ex_logout()
        assert auth.check_session() == False

    @pytest.mark.run(order=2)
    def test_login_again(self):
        assert auth.load_dumped_session() != False
    
    @pytest.mark.run(order=3)
    def test_logout_hard(self,monkeypatch):
        self.test_login_success(monkeypatch)
        auth.ex_logout(True)
        result = bool(auth.check_session()) or bool(auth.check_env())
        
        assert result == False
    
    @pytest.mark.skip
    def test_no_session(self):
        auth.load_dumped_session()

    @pytest.mark.run(order=5)
    def test_fail_login_wrong_account(self,monkeypatch):
        
        monkeypatch.setattr('libs.auth.get_username', lambda : 'user')
        monkeypatch.setattr('getpass.getpass', lambda x : 'pwd')
        with pytest.raises(SystemExit):
            auth.signin()
    
    @pytest.mark.run(order=6)
    def test_fresh_login(self,monkeypatch):
        load_dotenv("~/Documents/.restknot.env")
        os.rmdir("{}/restknot".format(FOLDER))
        user = os.environ.get('OS_USERNAME')
        pwd  = os.environ.get('OS_PASSWORD')
        monkeypatch.setattr('libs.auth.get_username', lambda  : user)
        monkeypatch.setattr('getpass.getpass', lambda x : pwd)
        assert auth.signin() == True