package orion.analytics.core.api.filter;

import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import java.io.IOException;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;

@Component
public class UserIDFilter extends OncePerRequestFilter
{
    @Override
    protected void doFilterInternal(HttpServletRequest req, HttpServletResponse res, FilterChain chain) throws ServletException, IOException
    {
        /*String authHeader = req.getHeader("Authorization");
        if(authHeader != null && authHeader.startsWith("Bearer "))
        {
            String token = authHeader.substring(7);
            String userID = jwtService.extractUserID(token);
            if(userID != null && SecurityContextHolder.getContext().getAuthentication() == null)
            {
                UserModel user = userService.loadUserByUserID(userID);
                if(jwtService.validateToken(token, user))
                {
                    UsernamePasswordAuthenticationToken auth = new UsernamePasswordAuthenticationToken(user, null, user.getAuthorities());
                    auth.setDetails(new WebAuthenticationDetailsSource().buildDetails(req));
                    SecurityContextHolder.getContext().setAuthentication(auth);
                }
            }
        }*/
        chain.doFilter(req, res);
    }
}
