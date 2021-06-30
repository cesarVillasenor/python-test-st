import operator
from django.shortcuts import render
from django.views.generic import TemplateView
from datetime import date, datetime


class DetectingChange(TemplateView):
    template_name = 'challenge.html'
    title = "Detecting Changes"
    dataset = [
        ("01/01/2020", False),
        ("01/02/2020", True),
        ("01/03/2020", True),
        ("01/04/2020", False),
        ("01/05/2020", False),
        ("01/06/2020", True),
        ("01/07/2020", False),
        ("01/08/2020", True),
        ("01/09/2020", True),
        ("01/10/2020", True),
    ]

    def get_context_data(self, **kwargs):
        """
        :param kwargs: parameter of the request
        :return: context of the request with the results
        """
        context = super(DetectingChange, self).get_context_data(**kwargs)
        last_status = ""
        results = []
        for row in self.dataset:
            if last_status == "":
                last_status = row[1]
                if last_status:
                    results.append((row[0], row[1]))
            if row[1] != last_status:
                last_status = row[1]
                if last_status:
                    results.append((row[0], row[1]))
        context["results"] = results
        return context


class SeasonProblem(TemplateView):
    template_name = 'challenge.html'
    title = "Seasons Problems"
    dataset = [
        ("113_8909896-6940269", "09/23/19", 1),
        ("114_0291773-7262677", "01/01/20", 1),
        ("114_0291773-7262697", "12/25/19", 1),
        ("114_9900513-7761000", "09/24/20", 1),
        ("112_5230502-8173028", "01/30/20", 1),
        ("112_7714081-3300254", "05/02/20", 1),
        ("114_5384551-1465853", "04/02/20", 1),
        ("114_7232801-4607440", "10/09/20", 1),
    ]
    seasons = [
        ("Spring", date(2000, 3, 19), date(2000, 6, 19)),
        ("Summer", date(2000, 6, 20), date(2000, 9, 21)),
        ("Fall", date(2000, 9, 22), date(2000, 12, 20)),
        ("Winter", date(2000, 12, 20), date(2001, 3, 18)),
    ]

    def get_year(self, record):
        return datetime.strptime(record[1], "%m/%d/%y").strftime("%y")

    def get_context_data(self, **kwargs):
        """from
        :param kwargs: parameter of the request
        :return: context of the request with the results
        """
        context = super(SeasonProblem, self).get_context_data(**kwargs)
        self.dataset = sorted(self.dataset, key=self.get_year, reverse=False)
        results = []
        year = 2000
        for row in self.dataset:
            date_row = datetime.strptime(row[1], "%m/%d/%y").replace(year=year).date()
            if self.seasons[0][1] <= date_row <= self.seasons[0][2]:
                season = self.seasons[0][0]
            elif self.seasons[1][1] <= date_row <= self.seasons[1][2]:
                season = self.seasons[1][0]
            elif self.seasons[2][1] <= date_row <= self.seasons[2][2]:
                season = self.seasons[2][0]
            else:
                season = self.seasons[3][0]
            results.append((row[0], season))
        context["results"] = results
        return context


class CustomOrderStatus(TemplateView):
    template_name = 'challenge.html'
    title = "Custom Order Status"
    dataset = [
        ("ORD_1567", "LAPTOP", "SHIPPED"),
        ("ORD_1567", "MOUSE", "SHIPPED"),
        ("ORD_1567", "KEYBOARD", "PENDING"),
        ("ORD_1234", "GAME", "SHIPPED"),
        ("ORD_1234", "BOOK", "CANCELLED"),
        ("ORD_1234", "BOOK", "CANCELLED"),
        ("ORD_9834", "SHIRT", "SHIPPED"),
        ("ORD_9834", "PANTS", "CANCELLED"),
        ("ORD_7654", "TV", "CANCELLED"),
        ("ORD_7654", "DVD", "CANCELLED"),
    ]

    def get_context_data(self, **kwargs):
        """
        :param kwargs: parameter of the request
        :return: context of the request with the results
        """
        context = super(CustomOrderStatus, self).get_context_data(**kwargs)
        results = []
        order = ""
        pending = False
        cancelled = 0
        order_counter = 0
        previous_order = ""
        for row in self.dataset:
            if order == "":
                order = row[0]
            if row[0] == order:
                order_counter += 1
                if row[2] == "CANCELLED":
                    cancelled += 1
                elif row[2] == "PENDING":
                    pending = True
                else:
                    pass
            else:
                if pending:
                    results.append((order, "PENDING"))
                elif cancelled == order_counter:
                    results.append((order, "CANCELLED"))
                else:
                    results.append((order, "SHIPPED"))
                pending = False
                cancelled = 0
                order_counter = 1
                order = row[0]
                if row[2] == "CANCELLED":
                    cancelled += 1
                elif row[2] == "PENDING":
                    pending = True
                else:
                    pass
        if len(self.dataset) > 0:
            if pending:
                results.append((row[0], "PENDING"))
            elif cancelled == order_counter:
                results.append((row[0], "CANCELLED"))
            else:
                results.append((row[0], "SHIPPED"))
        context["results"] = results
        return context
