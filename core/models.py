# from django.contrib.auth.models import User
# from django.db import models
#
#
# class Prediction(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     team_a_id = models.IntegerField()
#     team_b_id = models.IntegerField()
#     team_a_score = models.IntegerField()
#     team_b_score = models.IntegerField()
#
#
# class GameweekScore(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     season = models.IntegerField()
#     gameweek = models.IntegerField()
#     prediction = models.ForeignKey(Prediction, on_delete=models.CASCADE)
#     score = models.IntegerField()
