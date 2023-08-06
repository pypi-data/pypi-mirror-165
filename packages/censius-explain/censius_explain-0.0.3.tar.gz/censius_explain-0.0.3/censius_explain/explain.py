import warnings
import pandas as pd
import shap
warnings.filterwarnings('ignore')


class Explain:

    """
    This class is used to get explainability values for the features.
    The current version supports only shap explanations.
    Future releases will have support for other types of explanations.
    """

    def __init__(self, model):

        """
        Initialize the model
        """

        self.model=model

    def explain_model(self, features_x, modality = 'tabular', model_category = None,
                      features_train = None, explanation_type = 'shap'):

        """
        Calculate the explainability values and return it.
        """

        no_data_models=['decision_tree', 'xgboost', 'gb', 'random_forest']
        if explanation_type=='shap':
            if modality=='tabular':
                keys_list=[]
                values_list=[]
                for feat in features_x:
                    keys_list.append(feat['feature_name'])
                    values_list.append(feat['feature_value'])
               
                if model_category in no_data_models:

                    explainer = shap.Explainer(self.model)
                    shap_values =explainer.shap_values(pd.DataFrame([values_list]),
                                                       check_additivity = False)
                    
                else:
                    explainer = shap.KernelExplainer(self.model.predict, features_train)
                    shap_values = explainer.shap_values(pd.DataFrame([values_list]))
                shap_list=shap_values[0].tolist()
                if isinstance(shap_list[0],list):
                    shap_list=shap_values[0].tolist()[0]
                res=dict(zip(keys_list, shap_list))
                return res



