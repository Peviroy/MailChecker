# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 09:17:32 2020

@author: Uzin
"""

import os
os.chdir(os.path.split(os.path.realpath(__file__))[0])
import sys
sys.path.append(os.path.abspath(".."))
from model.MiltiNB import MultiNB_Wrapper


class TestMultiNBInstance:
    def test_generate_model(self):
        assert MultiNB_Wrapper.generate_model() is not None

    def test_IO(self):
        test_string0 = "for test000"
        test_string1 = "for test111"
        assert 'test_text.pickle' != MultiNB_Wrapper.save_model(test_string0, test_string1, "pickle", "test_model_text", "test_cv_model")
        assert 'test_text.model' != MultiNB_Wrapper.save_model(test_string0, test_string1, "joblib", "test_model_text", "test_cv_model")
        assert MultiNB_Wrapper.save_model(test_string0, test_string1, "error", "test_model_text", "test_cv_model") is None
        
        assert MultiNB_Wrapper.load_model('pickle', "test_model_text", "test_cv_model") is not None
        assert MultiNB_Wrapper.load_model('joblib', "test_model_text", "test_cv_model") is not None
        assert MultiNB_Wrapper.load_model('error', "test_model_text", "test_cv_model") is None
        out_file0 = MultiNB_Wrapper.load_model('pickle', "test_model_text", "test_cv_model")
        out_file1 = MultiNB_Wrapper.load_model('joblib', "test_model_text", "test_cv_model")
        print(out_file0)
        print(out_file1)
        
    def test_predict(self):
        try:
            t = MultiNB_Wrapper.predict("how are u!")
            print(t)
        except Exception as e:
            assert isinstance(e, FileNotFoundError)
        try:
            t = MultiNB_Wrapper.predict("free wkly low get now!!!!")
            print(t)
        except Exception as e:
            assert isinstance(e, FileNotFoundError)
            
    def test_get_alpha(self):
        assert MultiNB_Wrapper.get_alpha() is not None
        print(MultiNB_Wrapper.get_alpha() )
        
    def test_get_vector_from_text(self):
        assert MultiNB_Wrapper.get_vector_from_text("are u ok im u ours") is not None
        print(MultiNB_Wrapper.get_vector_from_text("are u ok im u ours") )
