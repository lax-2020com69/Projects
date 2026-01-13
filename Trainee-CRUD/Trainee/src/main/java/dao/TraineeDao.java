package dao;

import db.DBUtil;
import model.Trainee;

import java.sql.*;
import java.util.ArrayList;
import java.util.List;

public class TraineeDao {
    public boolean addTrainee(Trainee Trainee) {
        String sql = "INSERT INTO trainee (name, email, department, stipend) values (?,?,?,?)";

        try (Connection conn = DBUtil.getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql)) {

            stmt.setString(1, Trainee.getName());
            stmt.setString(2, Trainee.getEmail());
            stmt.setString(3, Trainee.getDepartment());
            stmt.setString(4, Trainee.getStipend());

            return stmt.executeUpdate() > 0;

        } catch (SQLException e) {
            e.printStackTrace();
            return false;
        }
    }

    public List<Trainee> getAllTrainee() {
        List<Trainee> list = new ArrayList<>();
        String sql = "SELECT * FROM trainee";

        try (Connection conn = DBUtil.getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql);
             ResultSet rs = stmt.executeQuery()) {
            while (rs.next()) {
                Trainee Trainee = new Trainee();
                Trainee.setId(rs.getInt("id"));
                Trainee.setName(rs.getString("name"));
                Trainee.setEmail(rs.getString("email"));
                Trainee.setDepartment(rs.getString("department"));
                Trainee.setStipend(rs.getString("stipend"));
                list.add(Trainee);
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return list;
    }

    public Trainee getAllTraineeById(int id) {
        String sql = "SELECT * FROM trainee Where id=?";
        Trainee t = null;

        try (Connection conn = DBUtil.getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql);) {
            stmt.setInt(1, id);
            try ( ResultSet rs = stmt.executeQuery()) {
                if (rs.next()) {
                    t = new Trainee();
                    t.setId(rs.getInt("id"));
                    t.setName(rs.getString("name"));
                    t.setEmail(rs.getString("email"));
                    t.setDepartment(rs.getString("department"));
                    t.setStipend(rs.getString("stipend"));
                }
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return t;
    }

    public boolean updateTrainee(Trainee Trainee) {
        String sql = "UPDATE trainee set name = ?, email = ?, department = ?, stipend = ? where id = ?";

        try (Connection conn = DBUtil.getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql)) {
            stmt.setString(1,Trainee.getName());
            stmt.setString(2,Trainee.getEmail());
            stmt.setString(3,Trainee.getDepartment());
            stmt.setString(4,Trainee.getStipend());
            stmt.setInt(5,Trainee.getId());
            return stmt.executeUpdate() > 0;
        } catch (SQLException e) {
            e.printStackTrace();
            return false;
        }
    }

    public boolean deleteTrainee(int id) {
        String sql = "DELETE FROM trainee where id = ?";

        try (Connection conn = DBUtil.getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql)) {
            stmt.setInt(1,id);
            return stmt.executeUpdate() > 0;
        } catch (Exception e) {
            e.printStackTrace();
            return false;
        }
    }
}
