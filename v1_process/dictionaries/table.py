ranges = [
        (0, 4, 0),
        (4, 16, 0.01),
        (16, 17, 0.012),
        (17, 18, 0.014),
        (18, 19, 0.016),
        (19, 20, 0.018),
        (20, float('inf'), 0.02)
        ]

uvtTable = [
              {
                "min" : 0,
                "max" : 95,
                "percentage" : 0,
                "subsValue" : 0,
                "addValue" : 0
              },
              {
                "min" : 95,
                "max" : 150,
                "percentage" : 0.19,
                "subsValue" : 95,
                "addValue" : 0
              },
              {
                "min" : 150,
                "max" : 360,
                "percentage" : 0.28,
                "subsValue" : 150,
                "addValue" : 10
              },
              {
                "min" : 360,
                "max" : 640,
                "percentage" : 0.33,
                "subsValue" : 360,
                "addValue" : 69
              },
              {
                "min" : 640,
                "max" : 945,
                "percentage" : 0.35,
                "subsValue" : 640,
                "addValue" : 162
              },
              {
                "min" : 945,
                "max" : 2300,
                "percentage" : 0.37,
                "subsValue" : 945,
                "addValue" : 268
              },
              {
                "min" : 2300,
                "max" : -1,
                "percentage" : 0.39,
                "subsValue" : 2300,
                "addValue" : 770
              }
            ]