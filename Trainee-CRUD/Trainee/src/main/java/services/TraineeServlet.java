package services;

import com.google.gson.Gson;
import dao.TraineeDao;
import model.Trainee;

import javax.servlet.annotation.WebServlet;
import javax.servlet.http.*;
import java.io.BufferedReader;
import java.io.IOException;
import java.util.List;

@WebServlet("/trainees/*")
public class TraineeServlet extends HttpServlet {

    private final Gson gson = new Gson();
    private final TraineeDao traineeDao = new TraineeDao();

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws IOException {
        response.setContentType("application/json");
        try (BufferedReader reader = request.getReader()) {
            Trainee trainee = gson.fromJson(reader, Trainee.class);
            boolean isSaved = traineeDao.addTrainee(trainee);

            if (isSaved) {
                response.setStatus(HttpServletResponse.SC_OK);
                response.getWriter().write("{\"message\":\"Trainee saved successfully\"}");
            } else {
                response.setStatus(HttpServletResponse.SC_INTERNAL_SERVER_ERROR);
                response.getWriter().write("{\"error\":\"Failed to insert trainee\"}");
            }
        }
    }

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws IOException {
        response.setContentType("application/json");

        String pathInfo = request.getPathInfo();
        if (pathInfo == null || pathInfo.equals("/")) {
            List<Trainee> list = traineeDao.getAllTrainee();
            response.getWriter().write(gson.toJson(list));
        } else {
            try {
                int id = Integer.parseInt(pathInfo.substring(1));
                Trainee trainee = traineeDao.getAllTraineeById(id);

                if (trainee != null) {
                    response.getWriter().write(gson.toJson(trainee));
                } else {
                    response.setStatus(HttpServletResponse.SC_NOT_FOUND);
                    response.getWriter().write("{\"error\":\"Trainee not found\"}");
                }
            } catch (NumberFormatException e) {
                response.setStatus(HttpServletResponse.SC_BAD_REQUEST);
                response.getWriter().write("{\"error\":\"Invalid ID format\"}");
            }
        }
    }

    @Override
    protected void doPut(HttpServletRequest request, HttpServletResponse response) throws IOException {
        response.setContentType("application/json");

        try (BufferedReader reader = request.getReader()) {
            Trainee trainee = gson.fromJson(reader, Trainee.class);

            if (trainee.getId() == 0) {
                response.setStatus(HttpServletResponse.SC_BAD_REQUEST);
                response.getWriter().write("{\"error\":\"Missing trainee ID\"}");
                return;
            }

            boolean isUpdated = traineeDao.updateTrainee(trainee);
            if (isUpdated) {
                response.getWriter().write("{\"message\":\"Trainee updated successfully\"}");
            } else {
                response.setStatus(HttpServletResponse.SC_NOT_FOUND);
                response.getWriter().write("{\"error\":\"Trainee not found\"}");
            }

        } catch (Exception e) {
            response.setStatus(HttpServletResponse.SC_BAD_REQUEST);
            response.getWriter().write("{\"error\":\"Invalid JSON: " + e.getMessage() + "\"}");
        }
    }

    @Override
    protected void doDelete(HttpServletRequest request, HttpServletResponse response) throws IOException {
        response.setContentType("application/json");
        String pathInfo = request.getPathInfo();

        if (pathInfo == null || pathInfo.equals("/")) {
            response.setStatus(HttpServletResponse.SC_BAD_REQUEST);
            response.getWriter().write("{\"error\":\"ID is required for delete\"}");
            return;
        }

        try {
            int id = Integer.parseInt(pathInfo.substring(1));
            boolean isDeleted = traineeDao.deleteTrainee(id);

            if (isDeleted) {
                response.getWriter().write("{\"message\":\"Trainee deleted successfully\"}");
            } else {
                response.setStatus(HttpServletResponse.SC_NOT_FOUND);
                response.getWriter().write("{\"error\":\"Trainee not found\"}");
            }

        } catch (NumberFormatException e) {
            response.setStatus(HttpServletResponse.SC_BAD_REQUEST);
            response.getWriter().write("{\"error\":\"Invalid ID format\"}");
        }
    }
}
