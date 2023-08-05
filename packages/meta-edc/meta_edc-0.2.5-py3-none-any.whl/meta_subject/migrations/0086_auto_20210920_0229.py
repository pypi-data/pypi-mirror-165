# Generated by Django 3.2.6 on 2021-09-19 23:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("edc_mnsi", "0002_historicalmnsi_mnsi"),
        ("meta_subject", "0085_auto_20210911_2036"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="historicalmnsi",
            name="examined_left_foot",
        ),
        migrations.RemoveField(
            model_name="historicalmnsi",
            name="examined_right_foot",
        ),
        migrations.RemoveField(
            model_name="mnsi",
            name="examined_left_foot",
        ),
        migrations.RemoveField(
            model_name="mnsi",
            name="examined_right_foot",
        ),
        migrations.AlterField(
            model_name="historicalmnsi",
            name="ankle_reflexes_left_foot",
            field=models.CharField(
                choices=[
                    ("present", "Present"),
                    ("present_with_reinforcement", "Present/Reinforcement"),
                    ("absent", "Absent"),
                    ("not_examined", "Not examined"),
                ],
                default="not_examined",
                help_text="If the MNSI assessment was not performed, or amputation prevents examination, respond with `not examined`.",
                max_length=35,
                verbose_name="Ankle reflexes, LEFT foot?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalmnsi",
            name="ankle_reflexes_right_foot",
            field=models.CharField(
                choices=[
                    ("present", "Present"),
                    ("present_with_reinforcement", "Present/Reinforcement"),
                    ("absent", "Absent"),
                    ("not_examined", "Not examined"),
                ],
                default="not_examined",
                help_text="If the MNSI assessment was not performed, or amputation prevents examination, respond with `not examined`.",
                max_length=35,
                verbose_name="Ankle reflexes, RIGHT foot?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalmnsi",
            name="mnsi_performed",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="Yes",
                help_text="If completion of patient history or physical assessment not possible, respond with `no` and provide reason below.",
                max_length=15,
                verbose_name="Is the MNSI assessment being performed?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalmnsi",
            name="monofilament_left_foot",
            field=models.CharField(
                choices=[
                    ("NORMAL", "Normal"),
                    ("reduced", "Reduced"),
                    ("absent", "Absent"),
                    ("not_examined", "Not examined"),
                ],
                default="not_examined",
                help_text="If the MNSI assessment was not performed, or amputation prevents examination, respond with `not examined`.",
                max_length=35,
                verbose_name="Monofilament, LEFT foot?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalmnsi",
            name="monofilament_right_foot",
            field=models.CharField(
                choices=[
                    ("NORMAL", "Normal"),
                    ("reduced", "Reduced"),
                    ("absent", "Absent"),
                    ("not_examined", "Not examined"),
                ],
                default="not_examined",
                help_text="If the MNSI assessment was not performed, or amputation prevents examination, respond with `not examined`.",
                max_length=35,
                verbose_name="Monofilament, RIGHT foot?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalmnsi",
            name="normal_appearance_left_foot",
            field=models.CharField(
                choices=[
                    ("Yes", "Yes"),
                    ("No", "No"),
                    ("not_examined", "Not examined"),
                ],
                default="not_examined",
                help_text="If the MNSI assessment was not performed, respond with `not examined`.",
                max_length=15,
                verbose_name="Does LEFT foot appear normal?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalmnsi",
            name="normal_appearance_right_foot",
            field=models.CharField(
                choices=[
                    ("Yes", "Yes"),
                    ("No", "No"),
                    ("not_examined", "Not examined"),
                ],
                default="not_examined",
                help_text="If the MNSI assessment was not performed, respond with `not examined`.",
                max_length=15,
                verbose_name="Does RIGHT foot appear normal?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalmnsi",
            name="ulceration_left_foot",
            field=models.CharField(
                choices=[
                    ("absent", "Absent"),
                    ("present", "Present"),
                    ("not_examined", "Not examined"),
                ],
                default="not_examined",
                help_text="If the MNSI assessment was not performed, or amputation prevents examination, respond with `not examined`.",
                max_length=35,
                verbose_name="Ulceration, LEFT foot?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalmnsi",
            name="ulceration_right_foot",
            field=models.CharField(
                choices=[
                    ("absent", "Absent"),
                    ("present", "Present"),
                    ("not_examined", "Not examined"),
                ],
                default="not_examined",
                help_text="If the MNSI assessment was not performed, or amputation prevents examination, respond with `not examined`.",
                max_length=35,
                verbose_name="Ulceration, RIGHT foot?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalmnsi",
            name="vibration_perception_left_toe",
            field=models.CharField(
                choices=[
                    ("present", "Present"),
                    ("decreased", "Decreased"),
                    ("absent", "Absent"),
                    ("not_examined", "Not examined"),
                ],
                default="not_examined",
                help_text="If the MNSI assessment was not performed, or amputation prevents examination, respond with `not examined`.",
                max_length=35,
                verbose_name="Vibration perception at great toe, LEFT foot?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalmnsi",
            name="vibration_perception_right_toe",
            field=models.CharField(
                choices=[
                    ("present", "Present"),
                    ("decreased", "Decreased"),
                    ("absent", "Absent"),
                    ("not_examined", "Not examined"),
                ],
                default="not_examined",
                help_text="If the MNSI assessment was not performed, or amputation prevents examination, respond with `not examined`.",
                max_length=35,
                verbose_name="Vibration perception at great toe, RIGHT foot?",
            ),
        ),
        migrations.AlterField(
            model_name="mnsi",
            name="abnormal_obs_left_foot",
            field=models.ManyToManyField(
                blank=True,
                related_name="_meta_subject_mnsi_abnormal_obs_left_foot_+",
                to="edc_mnsi.AbnormalFootAppearanceObservations",
                verbose_name="If NO, check all that apply to LEFT foot?",
            ),
        ),
        migrations.AlterField(
            model_name="mnsi",
            name="abnormal_obs_right_foot",
            field=models.ManyToManyField(
                blank=True,
                related_name="_meta_subject_mnsi_abnormal_obs_right_foot_+",
                to="edc_mnsi.AbnormalFootAppearanceObservations",
                verbose_name="If NO, check all that apply to RIGHT foot?",
            ),
        ),
        migrations.AlterField(
            model_name="mnsi",
            name="ankle_reflexes_left_foot",
            field=models.CharField(
                choices=[
                    ("present", "Present"),
                    ("present_with_reinforcement", "Present/Reinforcement"),
                    ("absent", "Absent"),
                    ("not_examined", "Not examined"),
                ],
                default="not_examined",
                help_text="If the MNSI assessment was not performed, or amputation prevents examination, respond with `not examined`.",
                max_length=35,
                verbose_name="Ankle reflexes, LEFT foot?",
            ),
        ),
        migrations.AlterField(
            model_name="mnsi",
            name="ankle_reflexes_right_foot",
            field=models.CharField(
                choices=[
                    ("present", "Present"),
                    ("present_with_reinforcement", "Present/Reinforcement"),
                    ("absent", "Absent"),
                    ("not_examined", "Not examined"),
                ],
                default="not_examined",
                help_text="If the MNSI assessment was not performed, or amputation prevents examination, respond with `not examined`.",
                max_length=35,
                verbose_name="Ankle reflexes, RIGHT foot?",
            ),
        ),
        migrations.AlterField(
            model_name="mnsi",
            name="mnsi_performed",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="Yes",
                help_text="If completion of patient history or physical assessment not possible, respond with `no` and provide reason below.",
                max_length=15,
                verbose_name="Is the MNSI assessment being performed?",
            ),
        ),
        migrations.AlterField(
            model_name="mnsi",
            name="monofilament_left_foot",
            field=models.CharField(
                choices=[
                    ("NORMAL", "Normal"),
                    ("reduced", "Reduced"),
                    ("absent", "Absent"),
                    ("not_examined", "Not examined"),
                ],
                default="not_examined",
                help_text="If the MNSI assessment was not performed, or amputation prevents examination, respond with `not examined`.",
                max_length=35,
                verbose_name="Monofilament, LEFT foot?",
            ),
        ),
        migrations.AlterField(
            model_name="mnsi",
            name="monofilament_right_foot",
            field=models.CharField(
                choices=[
                    ("NORMAL", "Normal"),
                    ("reduced", "Reduced"),
                    ("absent", "Absent"),
                    ("not_examined", "Not examined"),
                ],
                default="not_examined",
                help_text="If the MNSI assessment was not performed, or amputation prevents examination, respond with `not examined`.",
                max_length=35,
                verbose_name="Monofilament, RIGHT foot?",
            ),
        ),
        migrations.AlterField(
            model_name="mnsi",
            name="normal_appearance_left_foot",
            field=models.CharField(
                choices=[
                    ("Yes", "Yes"),
                    ("No", "No"),
                    ("not_examined", "Not examined"),
                ],
                default="not_examined",
                help_text="If the MNSI assessment was not performed, respond with `not examined`.",
                max_length=15,
                verbose_name="Does LEFT foot appear normal?",
            ),
        ),
        migrations.AlterField(
            model_name="mnsi",
            name="normal_appearance_right_foot",
            field=models.CharField(
                choices=[
                    ("Yes", "Yes"),
                    ("No", "No"),
                    ("not_examined", "Not examined"),
                ],
                default="not_examined",
                help_text="If the MNSI assessment was not performed, respond with `not examined`.",
                max_length=15,
                verbose_name="Does RIGHT foot appear normal?",
            ),
        ),
        migrations.AlterField(
            model_name="mnsi",
            name="ulceration_left_foot",
            field=models.CharField(
                choices=[
                    ("absent", "Absent"),
                    ("present", "Present"),
                    ("not_examined", "Not examined"),
                ],
                default="not_examined",
                help_text="If the MNSI assessment was not performed, or amputation prevents examination, respond with `not examined`.",
                max_length=35,
                verbose_name="Ulceration, LEFT foot?",
            ),
        ),
        migrations.AlterField(
            model_name="mnsi",
            name="ulceration_right_foot",
            field=models.CharField(
                choices=[
                    ("absent", "Absent"),
                    ("present", "Present"),
                    ("not_examined", "Not examined"),
                ],
                default="not_examined",
                help_text="If the MNSI assessment was not performed, or amputation prevents examination, respond with `not examined`.",
                max_length=35,
                verbose_name="Ulceration, RIGHT foot?",
            ),
        ),
        migrations.AlterField(
            model_name="mnsi",
            name="vibration_perception_left_toe",
            field=models.CharField(
                choices=[
                    ("present", "Present"),
                    ("decreased", "Decreased"),
                    ("absent", "Absent"),
                    ("not_examined", "Not examined"),
                ],
                default="not_examined",
                help_text="If the MNSI assessment was not performed, or amputation prevents examination, respond with `not examined`.",
                max_length=35,
                verbose_name="Vibration perception at great toe, LEFT foot?",
            ),
        ),
        migrations.AlterField(
            model_name="mnsi",
            name="vibration_perception_right_toe",
            field=models.CharField(
                choices=[
                    ("present", "Present"),
                    ("decreased", "Decreased"),
                    ("absent", "Absent"),
                    ("not_examined", "Not examined"),
                ],
                default="not_examined",
                help_text="If the MNSI assessment was not performed, or amputation prevents examination, respond with `not examined`.",
                max_length=35,
                verbose_name="Vibration perception at great toe, RIGHT foot?",
            ),
        ),
    ]
