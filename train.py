from age_pred_model import AgePredModel

if __name__ == "__main__":
    a = AgePredModel(model_name='res18_cls70',
                     new_training_process=False,
                     new_last_layer=True)
    a.train_model()
    